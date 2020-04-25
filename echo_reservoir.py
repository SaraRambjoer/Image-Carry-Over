import numpy
import scipy.sparse

class echo_reservoir:
    def __init__(self, adjacency_matrix, input_producer, output_consumer, matrix_width, matrix_height, chaos_factor, decay):
        self.adjacency_matrix = adjacency_matrix
        self.input_producer = input_producer
        self.output_consumer = output_consumer
        self.timestep = 0
        self.matrix_width = matrix_width
        self.matrix_height = matrix_height
        self.node_values = numpy.zeros([matrix_width * matrix_height], dtype=float)
        self.chaos_factor = chaos_factor
        self.decay = decay

    def do_timestep(self):
        update = scipy.sparse.csr_matrix.dot(self.adjacency_matrix, self.node_values)/(self.matrix_width * self.matrix_height) # removing division causes overflow in line 19 - not sure how but node values greater than 1 seem to be carried over form previous iterations?
        self.node_values = self.input_producer(self.timestep) + self.chaos_factor*update*(1-update)  # logistic function w/ chaos valued parameter
        check = self.node_values >= 1.0
        if True in check:
            self.node_values = (self.node_values-min(self.node_values))/(max(self.node_values) - min(self.node_values)) # map to range [0, 1], prevents overflow
        self.output_consumer(self.node_values)
        self.timestep += 1

    def run(self, timesteps):
        for num in range(self.timestep, timesteps):
            self.do_timestep()

