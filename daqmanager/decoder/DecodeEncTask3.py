import struct
import os
from PyQt4.QtCore import pyqtSignal, SIGNAL, QThread
import shutil
from common.sqliteutils import DaqDB
import itertools
from datautils import *

def c2h(d):
    return d.encode(hex)

class DecodeEncTask(QThread):
    # QThread.__init__(self)
    signalNumOfRecords=pyqtSignal(int)
    signalCommit=pyqtSignal()

    TAILSYMBC="3C3C"
    # HEADER_STAT_DUMP_INIT="A7E8"
    # HEADER_STAT_DUMP_DATA="A7E1"
    HEADER_STAT="A8A7"
    HEADER_ENC="FCA7"


    DB_COMMIT_INTERVAL=5

    # current state machine
    #   enc mo1 mo2 15 25 35 45 55 65 85
    #   enc mo1 mo2 12 22 32 42 52 62
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   enc mo1 mo2 14 24 34 44 54 64 84
    #   enc mo1 mo2 16 26 36 46 56 66
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   enc mo1 mo2 12 22 32 42 52 62
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   enc mo1 mo2 16 26 36 46 56 66
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   rIdx wIdx counter 3C3C

    # DAQ_FORMAT_LIST=[ ">LHH","s<HBs<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH","s<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH",
    #                    ">LHH",
    #                    ">LHH","s<HBs<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH","s<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH",
    #                    ">LHH",
    #                    ">LHH","s<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH",
    #                    ">LHH",
    #                    ">LHH","s<HBs<HBs<HBs<HBs<HBs<HB",
    #                    ">LHH",
    #                    ">LHH",
    #                    ">HHL2s",
    # ]

    #bakcup
    DAQ_FORMAT_LIST=[ ">LHH","sHBsHBsHBsHBsHBsHBsHB",
                       "LHH","sHBsHBsHBsHBsHBsHB",
                       "LHH",
                       "LHH",
                       "LHH",
                       "LHH",
                       "LHH","sHBsHBsHBsHBsHBsHBsHB",
                       "LHH","sHBsHBsHBsHBsHBsHB",
                       "LHH",
                       "LHH",
                       "LHH",
                       "LHH",
                       "HHL2s",
                ]
    SENSE=['<sHB']
    ADU=['>HHL2s']
    ENC=['>LHH']
    lFormat=[
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,
        ENC,
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,
        ENC,
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,
        ENC,
        ENC,SENSE,SENSE,SENSE,SENSE,SENSE,SENSE,
        ENC,
        ENC,
        ADU,
    ]
    # ADU_SIZE= struct.calcsize(struct.calcsize("".join(ADU)))

    # STATE MACHINE CALIB
    CAL_FORMAT_LIST=[">2sHHHHH",
                "HHHHHHHH",
                "HHHHHHHH",
                "H2sHHHHHH",
                "HHHH2sHHH",
                "HHHHHHHH",
                "HHHH2sHHH",
                "HHHHHHHH",
                "HHHHHHHH",
                "HHH2sHHHH",
                "HHHH2sHHH",
                "HHHHHHHH",
                "HHHH2sHH2sL"]

    daq_fmt="".join(DAQ_FORMAT_LIST)
    DAQ_BUFFER_SIZE= struct.calcsize(daq_fmt)


    def calc_struct_size(self):
        lFormats=self.lFormat
        total=0
        for format in lFormats:
            total += struct.calcsize("".join(format))
        print total

    def __del__(self):
        ""
        # self.db.close(self)

    def __init__(self):
        ""
        QThread.__init__(self)
        self.numRecords=0
        self.currBytes=0
        self.totalBytes=0
        self.currFile=""
        self.db=DaqDB("../enc.db")
        self.pdb=DaqDB("../daq.db")
        
        # self.connect(self,SIGNAL("task_decode()"),self.parse_enc,file)

    def commit(self):
        ""
        self.db.commit()
                        # self.numRecords=num_recs
                        # self.currBytess=
        # self.emit(SIGNAL("decoded_sets()"))
        self.signalCommit.emit()
        self.signalNumOfRecords.emit(self.numRecords)


    # find the end of first header
    def seek_until(self,fh,file_size,start_pos):
      pre=start_pos
      while (pre < file_size):
        bytes=fh.read(2).encode("hex").upper()

        if bytes == self.TAILSYMBC:
          break
        else:
          pre+=2

      return fh.tell()


    def get_next_record(self,fh,file_size,start,estimate,margin=6):
        pos_s=start
        dr=fh.read(estimate - margin)

        while(pos_s+estimate < file_size):
            dr1=fh.read(2)
            hexsymb=dr1.encode("hex").upper()

            dr=dr+dr1
            if hexsymb == self.TAILSYMBC:
                break

        return hexsymb,dr

    # clean off artifiacts
    def reject_artifacts(self,dr):
        ""
        ndr=dr.encode("hex")
        ndr=ndr.replace("e7e7","")
        # print ndr
        # print len(ndr)
        #
        # a=ndr[0:424]
        # b=ndr[896:920]
        # disgard=ndr[424:1246]
        #
        # c= a+b
        # print c
        ndr=ndr.decode("hex")


        return ndr

    def remove_tuple(self,original_tuple, element_to_remove):
        new_tuple = []
        for s in list(original_tuple):
            if not s == element_to_remove:
                new_tuple.append(s)
        return tuple(new_tuple)



    # def insert(self):
    #     idx={}
    #     idx.update({
    #     "enc":32,
    #     "mo":16,
    #     "p":24,
    #     "h":11,
    #     "pt":24,
    #     "ht":11,
    #     "rIdx":16,
    #     "wIdx":16,
    #     "counter":32})

    def convert_resolution(self,dr):
        ""
        ndr=list()
        cdr = itertools.chain(dr)

    # current state machine
    #   enc mo1 mo2 15 25 35 45 55 65 85
    #   enc mo1 mo2 12 22 32 42 52 62
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   enc mo1 mo2 14 24 34 44 54 64 84
    #   enc mo1 mo2 16 26 36 46 56 66
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   enc mo1 mo2
    #   rIdx wIdx counter 3C3C

    #   hum values are 11bit
    #   pres values are 24bit
    # 2 - temp
    # 6 - pres
    #
    # 4 - temp
    # 5 - hum

  #   val = 66

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],11,5))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))
        ndr.append(cdr.next());ndr.append(bin_to_int([cdr.next(),cdr.next()],24))

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())
        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())

        ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next());ndr.append(cdr.next())

        return ndr



    def parse_enc(self,file,file_index):
        ""
        file_size=os.stat(file).st_size
        print "Opening file %s size %s" % (file, file_size)
        
        with open(file,'rb') as fh:
          pos_s=self.seek_until(fh,file_size,0)

          self.num_recs=0
          self.bad_recs=0
          self.currBytes=0
          while(True):
            try:
                pos_s=fh.tell()
                self.file_pos=pos_s

                if pos_s+self.DAQ_BUFFER_SIZE > file_size:
                    break

                recordType,chunk=self.get_next_record(fh,file_size,pos_s,self.DAQ_BUFFER_SIZE)
                chunk=self.reject_artifacts(chunk)

                ### check chunk is valid
                length=len(chunk)

                # print chunk.encode('hex')
                if length != self.DAQ_BUFFER_SIZE:
                    self.bad_recs = self.bad_recs+1

                    self.seek_until(fh,file_size,pos_s)
                else:

                    if recordType == self.TAILSYMBC:
                        rec=struct.unpack(self.daq_fmt,chunk)

                    rec=self.convert_resolution(rec)

                    ### add in processor info ###
                    timestamp=''


                    ####### 1 #######
                    # TEMP SENSE
                    rechash={}
                    # print 'numbering char'
                    # % - 25, 5 - 35, E - 45, U - 55, e - 65
                    hl=[rec[3],rec[5],rec[7],rec[9],rec[11],rec[13],rec[15]]
                    # print hl
                    hl=[rec[4],rec[6],rec[8],rec[10],rec[12],rec[14],rec[16]]


                    # l=[c2h(x) for x in hl]
                    # print l
                    rechash.update({"encoder_counter":rec[0], "mo1":rec[1], "mo2":rec[2],
                                    'c1_s5':rec[4], 'c2_s5':rec[6], 'c3_s5':rec[8], 'c4_s5':rec[10],
                                   'c5_s5':rec[12], 'c6_s5':rec[14], 'c8_s5':rec[16]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    # PTEMP
                    rechash={}

                    # print 'numbering char'
                    # " - 22, 2 - 32,
                    hl=[ rec[20],rec[22],rec[24],rec[26],rec[28],rec[30]]
                    # print hl
                    hl=[rec[21],rec[23],rec[25],rec[27],rec[29],rec[31]]
                    # print hl

                    print "POS:",self.file_pos,hex(self.file_pos)
                    # print hex(hl[0]),hex(hl[2])
                    print hex(hl[0])
                    # print hl[0],hl[2]
                    print hl
                    rechash.update({ 'encoder_counter':rec[17], "mo1":rec[18], "mo2":rec[19],
                                    'c1_s2':rec[21], 'c2_s2':rec[23], 'c3_s2':rec[25],'c4_s2':rec[27],
                                    'c5_s2':rec[29], 'c6_s2':rec[31]})

                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}

                    rechash.update({ 'encoder_counter':rec[32], "mo1":rec[33], "mo2":rec[34]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}


                    rechash.update({ 'encoder_counter':rec[35], "mo1":rec[36], "mo2":rec[37]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}

                    rechash.update({ 'encoder_counter':rec[38], "mo1":rec[39], "mo2":rec[40]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}


                    rechash.update({ 'encoder_counter':rec[41], "mo1":rec[42], "mo2":rec[43]})
                    self.db.insert_dict("enc",rechash)


                    ####### 2 #######
                    rechash={}
                    # HUMIDITY
                    # print 'numbering char'
                    # " - 22, 2 - 32, b - 62
                    hl=[ rec[47],rec[49],rec[51],rec[53],rec[55],rec[57],rec[59]]
                    # print hl
                    hl=[rec[48],rec[50],rec[52],rec[54],rec[56],rec[58],rec[60]]
                    # print hl

                    rechash.update({"encoder_counter":rec[44], "mo1":rec[45], "mo2":rec[46],
                                    'c1_s4':rec[48], 'c2_s4':rec[50], 'c3_s4':rec[52], 'c4_s4':rec[54],
                                   'c5_s4':rec[56], 'c6_s4':rec[58], 'c8_s4':rec[60]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    # PPRES
                    rechash={}
                    # print 'numbering char'
                    # " - 22, 2 - 32, b - 62
                    hl=[ rec[64],rec[66],rec[68],rec[70],rec[72],rec[75]]
                    # print hl
                    hl=[ rec[65],rec[67],rec[69],rec[71],rec[73],rec[75]]
                    # print hl

                    rechash.update({ 'encoder_counter':rec[61], "mo1":rec[62], "mo2":rec[63],
                                    'c1_s6':rec[65], 'c2_s6':rec[67], 'c3_s6':rec[69],'c4_s6':rec[71],
                                    'c5_s6':rec[73], 'c6_s6':rec[75]})

                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}
                    rechash.update({ 'encoder_counter':rec[76], "mo1":rec[77], "mo2":rec[78]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}
                    rechash.update({ 'encoder_counter':rec[79], "mo1":rec[80], "mo2":rec[81]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}
                    rechash.update({ 'encoder_counter':rec[82], "mo1":rec[83], "mo2":rec[84]})
                    self.db.insert_dict("enc",rechash)

                    ###
                    rechash={}
                    rechash.update({ 'encoder_counter':rec[85], "mo1":rec[86], "mo2":rec[87]})
                    self.db.insert_dict("enc",rechash)

                    ### 5 ###
                    rechash={}

                    rechash.update({'wIdx':rec[88], 'rIdx':rec[89], 'counter':rec[90], 'tailsymb':rec[91],
                                    'timestamp':timestamp})
                    # rechash.update({'file_index':file_index, 'packet_len':length, 'file_pos':self.file_pos})
                    rechash.update({'file_index':file_index, 'packet_len':length})
                    self.db.insert_dict("enc",rechash)

                    self.num_recs += 1

                    if self.num_recs % self.DB_COMMIT_INTERVAL == 0 and self.num_recs > 0 :
                        print "commit %s" % self.num_recs
                        self.db.commit()
                        # self.numRecords=num_recs
                        self.currBytess=self.currBytes+length
                        # self.emit(SIGNAL("decoded_sets()"))
                

            except Exception,e:
              print "read error: "+ str(e)


if __name__ == '__main__':

    os.remove('../enc.db')
    shutil.copy('../daq.db','../enc.db')
    task=DecodeEncTask()
    task.calc_struct_size()
    task.parse_enc("../client/data/20000101_000254.enc",0)



