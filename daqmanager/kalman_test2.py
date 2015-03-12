from filterutils import KalmanFilter

if __name__ == "__main__":
    import random
    iteration_count = 500

    actual_values = [-0.37727 + j * j * 0.00001 for j in xrange(iteration_count)]
    noisy_measurement = [random.random() * 2.0 - 1.0 + actual_val for actual_val in actual_values]

    # in practice we would take our sensor, log some readings and get the
    # standard deviation
    import numpy
    measurement_standard_deviation = numpy.std([random.random() * 2.0 - 1.0 for j in xrange(iteration_count)])

    # The smaller this number, the fewer fluctuations, but can also venture off
    # course...
    process_variance = 1e-3
    estimated_measurement_variance = measurement_standard_deviation ** 2  # 0.05 ** 2
    kalman_filter = KalmanFilter(process_variance, estimated_measurement_variance)
    posteri_estimate_graph = []

    for iteration in xrange(1, iteration_count):
        kalman_filter.input_latest_noisy_measurement(noisy_measurement[iteration])
        posteri_estimate_graph.append(kalman_filter.get_latest_estimated_measurement())

    import pylab
    pylab.figure()
    pylab.plot(noisy_measurement, color='r', label='noisy measurements')
    pylab.plot(posteri_estimate_graph, 'b-', label='a posteri estimate')
    pylab.plot(actual_values, color='g', label='truth value')
    pylab.legend()
    pylab.xlabel('Iteration')
    pylab.ylabel('Voltage')
    pylab.show()