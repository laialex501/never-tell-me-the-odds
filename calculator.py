from numpy.random import randint
from numpy import mean
from numpy import median
from matplotlib import pyplot as plt

# Each dice outcome is represented as a string. Multiple characters indicate multiple instances of results. 
# S = Success, A = Advantage, C = Triumph, F = Failure, T = Threat, D = Despair

ABILITY = ['', 'S', 'S', 'SS', 'A', 'A', 'SA', 'AA']
PROFICIENCY = ['', 'S', 'S', 'SS', 'SS', 'A', 'SA', 'SA', 'SA', 'AA', 'AA', 'C']
DIFFICULTY = ['', 'F', 'FF', 'T', 'T', 'T', 'TT', 'FT']
CHALLENGE = ['', 'F', 'F', 'FF', 'FF', 'T', 'T', 'FT', 'FT', 'TT', 'TT', 'D']
BOOST = ['', '', 'S', 'SA', 'AA', 'A']
SETBACK = ['', '', 'F', 'F', 'T', 'T']
DICE_TYPES = {'Ability': ABILITY, 'Proficiency': PROFICIENCY, 'Difficulty': DIFFICULTY, 'Challenge': CHALLENGE, 'Boost': BOOST, 'Setback': SETBACK}

class Dice:

    def __init__(self, name):
        if not (name in DICE_TYPES.keys()):
            raise ValueError('{name} is not a valid dice name'.format(name=name))
        self.name = name
        self.outcomes = DICE_TYPES[name]
        self.faces = len(self.outcomes)

    def roll(self):
        i = randint(0, self.faces)
        return self.outcomes[i]

    def __str__(self):
        return 'Dice Name: {name}, Faces: {faces}, Outcomes: {outcomes}'.format(name=self.name, faces=self.faces, outcomes=self.outcomes)

class Result:
    def __init__(self):
        self.success, self.advantage, self.triumph, self.despair = 0, 0, 0, 0

    # Takes in a Result object and a Dice object. Rolls one die of the specified type and adds the outcome to itself
    def roll(self, die):
        # If die is a string, returns a Dice object to roll corresponding to that string
        
        if isinstance(die, str):
            try:
                die = Dice(die)
            except ValueError as v:
                print(v)
        
        res = die.roll()
        for i in res:
            if i == 'S':
                self.success += 1
            elif i == 'F':
                self.success -= 1
            elif i == 'A':
                self.advantage += 1
            elif i == 'T':
                self.advantage -= 1
            elif i == 'C':
                self.success += 1
                self.triumph += 1
            elif i == 'D':
                self.success -= 1
                self.despair += 1

    # Expects dice_pool to be a dictionary of dice name as keys and a tuple of (Dice, int) values indicating the dice to roll and the number of times to roll it
    def roll_dice(self, dice_pool):
        for die, times in dice_pool.values():
            for _ in range(0, times):
                self.roll(die)

    def get_arr(self):
        return [self.success, self.advantage, self.triumph, self.despair]

    def get(self):
        return {'success': self.success, 'advantage': self.advantage, 'triumph': self.triumph, 'despair': self.despair}

    def get_attr(self, attr_names):
        output = {}
        for attr in attr_names:
            if attr == 'success':
                output['success'] = self.success
            elif attr == 'advantage':
                output['advantage'] = self.advantage
            elif attr == 'triumph':
                output['triumph'] = self.triumph
            elif attr == 'despair':
                output['despair'] = self.despair
            else:
                raise ValueError('No attribute named {attr} found'.format(attr=attr))
        return output

    # Returns true if there is a positive number of the desired attributes in this result
    def match(self, attr_names):
        output = True
        for attr in attr_names:
            if attr == 'success':
                output = (output) and (self.success > 0)
            elif attr == 'failure':
                output = (output) and (self.success <= 0)
            elif attr == 'advantage':
                output = (output) and (self.advantage > 0)
            elif attr == 'threat':
                output = (output) and (self.advantage < 0)
            elif attr == 'triumph':
                output = (output) and (self.triumph > 0)
            elif attr == 'despair':
                output = (output) and (self.despair > 0)
            else:
                raise ValueError('No attribute named {attr} found'.format(attr=attr))
        return output

def str_dice_pool_to_dice_pool(str_dice_pool):
    dice_pool = {}
    for name, number in str_dice_pool.items():
        if not isinstance(name, str):
            raise TypeError('dice names must be strings')
        die = Dice(name)
        dice_pool[name] = (die, number)
    return dice_pool

# Expects dice_pool to be a mapping of dice names as strings to the number of each dice
def estimate_probability(str_dice_pool, attr_names, sample_size=100, num_samples=10, log=False):
    # Estimate the probability of getting the requested attributes on a sample of a given size by counting
    def estimate_prob_sample(dice_pool, attr_names, sample_size):
        count = 0
        for _ in range(0, sample_size):
            res = Result()
            res.roll_dice(dice_pool)
            if (res.match(attr_names)):
                count +=1

        prob = count / sample_size
        return prob

    #Convert a dice pool with strings into a dice pool of (Dice, int) tuples indicating the correct dice and the number of times to roll it
    dice_pool = str_dice_pool_to_dice_pool(str_dice_pool)

    # Collects the sample probabilities from a given number of samples
    estimates = [estimate_prob_sample(dice_pool, attr_names, sample_size) for _ in range(0, num_samples)]
    
    # Collects the mean of the sample probabilities, justified by the CLT to converge to the sample mean
    samples_mean = mean(estimates)

    # Create a string to report the type of query that was made
    roll_str = ''
    for name, number in str_dice_pool.items():
        roll_str += '{0}: {1}, '.format(name, number)

    # Report the query and result
    if (log):
        print('Mean Probability of a positive number of {attr_names} on the roll "{roll_str}" with {num_samples} samples of size size {sample_size} is {mean}'.format(
            attr_names = attr_names, roll_str = roll_str, num_samples = num_samples, sample_size = sample_size, mean = str(round(samples_mean*100)) + "%"))

    return samples_mean

"""str_dice_pool = {'Ability': 2, 'Proficiency': 2, 'Difficulty': 2, 'Challenge': 0, 'Boost': 0, 'Setback': 0}
attr_names = ['success']
sample_size = 1000
num_samples = 10
log=True
estimate_probability(str_dice_pool, attr_names, sample_size, num_samples, log)"""

