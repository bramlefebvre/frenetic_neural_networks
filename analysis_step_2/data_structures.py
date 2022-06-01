class TrainingResult:
    def __init__(self, exuberant_system_id, success, number_of_states, number_of_patterns, driving_value,
                 initial_activity_parameter_factor, travel_time, algorithm, learning_rate, 
                 desired_residence_time, training_set_size, performance, calculation_duration):
        self.exuberant_system_id = exuberant_system_id
        self.success = success
        self.number_of_states = number_of_states
        self.number_of_patterns = number_of_patterns
        self.driving_value = driving_value
        self.initial_activity_parameter_factor = initial_activity_parameter_factor
        self.travel_time = travel_time
        self.algorithm = algorithm
        self.learning_rate = learning_rate
        self.desired_residence_time = desired_residence_time
        self.training_set_size = training_set_size
        self.performance = performance
        self.calculation_duration = calculation_duration


