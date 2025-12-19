import pylab as pl
import random

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """

def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title) -> None:
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()

def make_two_curve_plot(x_coords,y_coords1,y_coords2,
                        y_name1,y_name2,x_label,
                        y_label,title) -> None:
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()

class SimpleBacteria(object):
    def __init__(self:SimpleBacteria, birth_prob:float, death_prob:float) -> None:
        self.birth_prob:float = birth_prob
        self.death_prob:float = death_prob

    def is_killed(self:SimpleBacteria) -> bool:
        return random.random() < self.death_prob

    def reproduce(self:SimpleBacteria, pop_density:float) -> SimpleBacteria | None:
        if random.random() < self.birth_prob * (1 - pop_density):
            return SimpleBacteria(self.birth_prob,self.death_prob)
        else:
            return None

class Patient(object):
    def __init__(self:Patient, bacteria:list[SimpleBacteria], max_pop:int) -> None:
        self.bacteria:list[SimpleBacteria] = bacteria
        self.max_pop:int = max_pop

    def get_total_pop(self:Patient) -> int:
        return len(self.bacteria)

    def update(self:Patient) -> int:
        survived:list[SimpleBacteria] = []
        for b in self.bacteria:
            if not b.is_killed():
                survived.append(b)
        pop_density:float = len(survived) / self.max_pop
        new_bacteria:list[SimpleBacteria] = []
        for b in survived:
            new_bacteria.append(b)
            child = b.reproduce(pop_density)
            if child:
                new_bacteria.append(child)
        self.bacteria:list[SimpleBacteria] = new_bacteria
        return self.get_total_pop()

def calc_pop_avg(populations:list, n:int) -> float:
    total:int = 0
    for p in populations:
        total += p[n]
    return total / len(populations)

def simulation_without_antibiotic(num_bacteria:int, max_pop:int, birth_prob:float,
                                  death_prob:float, num_trials:int) -> list:
    populations:list[list[int]] = []
    for i in range(num_trials):
        bacteria:list[SimpleBacteria] = []
        for _ in range(num_bacteria):
            bacteria.append(SimpleBacteria(birth_prob, death_prob))
        patient = Patient(bacteria, max_pop)
        population:list[int] = []
        for n in range(300):
            population.append(patient.get_total_pop())
            patient.update()
        populations.append(population)
    
    x_coords:list[int] = list(range(300))
    y_coords:list[float] = [calc_pop_avg(populations, n) for n in x_coords]
    make_one_curve_plot(x_coords, y_coords, x_label="Time Step", y_label="Avg Population", title="Simulation - No Antibiotic")
    return populations

populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)

def calc_pop_std(populations:list[list[int]], t:int) -> float:
    mean:float = calc_pop_avg(populations, t)
    mse:float = [(x[t] - mean)**2 for x in populations]
    variance:float = sum(mse)/len(populations)
    st_dev:float = variance**0.5
    return st_dev

def calc_95_ci(populations:list[list[int]], t:int) -> tuple[float]:
    mean:float = calc_pop_avg(populations, t)
    st_dev = calc_pop_std(populations, t)
    sem:float = st_dev / len(populations)**0.5
    return (mean, 1.96 * sem)

class ResistantBacteria(SimpleBacteria):
    def __init__(self:ResistantBacteria, birth_prob:float, death_prob:float, 
                 resistant:bool, mut_prob:float) -> None:
        super().__init__(birth_prob, death_prob)
        self.resistant:bool = resistant
        self.mut_prob:float = mut_prob

    def get_resistant(self:ResistantBacteria) -> bool:
        return self.resistant

    def is_killed(self:ResistantBacteria) -> bool:
        if self.resistant:
            return super().is_killed()
        else:
            return random.random() < self.death_prob / 4

    def reproduce(self:ResistantBacteria, pop_density:float) -> ResistantBacteria | None:
        if random.random() < self.birth_prob * (1 - pop_density):
            if random.random() < self.mut_prob * (1 - pop_density):
                return ResistantBacteria(self.birth_prob, self.death_prob, True, self.mut_prob)
            else:
                return ResistantBacteria(self.birth_prob, self.death_prob, self.resistant, self.mut_prob)
        else:
            return None

class TreatedPatient(Patient):
    def __init__(self:TreatedPatient, bacteria:list[ResistantBacteria], max_pop:int) -> None:
        super().__init__(bacteria, max_pop)
        self.on_antibiotic:bool = False

    def set_on_antibiotic(self:TreatedPatient) -> None:
        self.on_antibiotic = True

    def get_resist_pop(self:TreatedPatient) -> int:
        return sum(1 for b in self.bacteria if b.get_resistant())

    def update(self:TreatedPatient) -> int:
        survived:list[ResistantBacteria] = []
        for b in self.bacteria:
            if not b.is_killed():
                survived.append(b)
        if self.on_antibiotic == True:
            new_survived = [b for b in survived if b.get_resistant()]
            survived = new_survived
        pop_density:float = len(survived) / self.max_pop
        new_bacteria:list[ResistantBacteria] = []
        for b in survived:
            new_bacteria.append(b)
            child = b.reproduce(pop_density)
            if child:
                new_bacteria.append(child)
        self.bacteria:list[ResistantBacteria] = new_bacteria
        return self.get_total_pop()

def simulation_with_antibiotic(num_bacteria:int,
                               max_pop:int,
                               birth_prob:float,
                               death_prob:float,
                               resistant:bool,
                               mut_prob:float,
                               num_trials:int) -> tuple[list, list]:
    populations:list[list[int]] = []
    resistant_populations:list[list[int]] = []
    for i in range(num_trials):
        bacteria:list[SimpleBacteria] = []
        for _ in range(num_bacteria):
            bacteria.append(ResistantBacteria(birth_prob, death_prob, resistant, mut_prob))
        patient = TreatedPatient(bacteria, max_pop)
        population:list[int] = []
        resistant_population:list[int] = []
        for n in range(150):
            population.append(patient.get_total_pop())
            resistant_population.append(patient.get_resist_pop())
            patient.update()
        patient.set_on_antibiotic()
        for o in range(250):
            population.append(patient.get_total_pop())
            resistant_population.append(patient.get_resist_pop())
            patient.update()
        populations.append(population)
        resistant_populations.append(resistant_population)
    
    x_coords:list[int] = list(range(400))
    y_coords1:list[float] = [calc_pop_avg(populations, n) for n in x_coords]
    y_coords2:list[float] = [calc_pop_avg(resistant_populations, n) for n in x_coords]
    make_two_curve_plot(x_coords, y_coords1, y_coords2,
                        y_name1="Total Population", y_name2="Resistant Population",
                        x_label="Time Step", y_label="Avg Population",
                        title="Simulation - With Antibiotic")
    return (populations,resistant_populations)

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.3,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
