import random


class Place:
    """
        Place in a Petri Net.

        Atributes
        ---------
        name: string
            Places name identifier.
        M: int
            Amount of tokens currently located in the place.
    """
    def __init__(self, name, M=0):
        self.name = name
        self.M = M

    def add_token(self, amount):
        """
        Add tokens to place.

        Parameters
        ----------
        amount: int
            Amount of tokens to add.
        """
        self.M += amount

    def remove_token(self, amount):
        """
        Remove tokens from place.

        Parameters
        ----------
        amount: int
            Amount of tokens to add.
        """
        self.M -= amount

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.__str__() == other.__str__()

class Arch:
    """
        Arch in a Petri Net.

        Atributes
        ---------
        place: Place
            Place connected to the arch.
        weight: int
            Amount of tokens removed from the place (input arch) or added to
            the place (output arch), when a transition is fired.
    """
    def __init__(self, place, weight):
        self.place = place
        self.weight = weight

class Transition:
    """
        Transition in a Petri net.

        Atributes
        ---------
        name: string
            Transition name identifier.
        inputs: list[Arch]
            List of input archs connected to the transition.
        outputs: list[Arch]
            List of output archs connected to the transition.
    """
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def is_enabled(self):
        """
            Check if a transition has met the conditions to be fired.

            Returns
            -------
            is_enabled: bool
                True if transition is enabled, false otherwise.
        """
        for arch in self.inputs:
            if arch.place.M < arch.weight:
                return False
        return True

    def fire(self):
        """
            Transition firing procedure.
        """
        if not self.is_enabled():
            return

        print('--Prijelaz {} je aktiviran--'.format(self.name))

        for arch in self.inputs:
            arch.place.remove_token(arch.weight)
            print('Uklanjanje značaka (količina = {}) sa mjesta {}'.\
                  format(arch.weight, arch.place))

        for arch in self.outputs:
            arch.place.add_token(arch.weight)
            print('Postavljanje značaka (količina = {}) na mjesto {}'.\
                  format(arch.weight, arch.place))

        print('--Prijelaz {} je izvršen--\n'.format(self.name))

    def __str__(self):
        return self.name


class PetriNet:

    def __init__(self, P, T, F, arch_list=[]):
        """
            Petri Net class, holds logic for simulating the behaviour and
            parsing definitions.

            Attributes
            ----------
            P: list[Place]
                Places in Petri Net.
            T: list[Transition]
                Transitions in Petri Net.
            F: list[Arch]
                Archs in Petri Net.
            arch_list: list[tuple]
                Arch list better suited for string formatting.
        """
        self.P = P
        self.T = T
        self.F = F
        self.arch_list = arch_list

    def run(self):
        """
            Run the Petri Net simulation.
        """
        print('\n Početak simulacije Petrijeve mreže\n')
        print('Definicija:\n{}\n'.format(self.__str__()))
        print('Početno stanje:\n{}\n---------\n'.format(self.get_M_as_string()))

        transitions_available = True

        while transitions_available: 
            transitions_available = False
            for transition in random.sample(self.T,len(self.T)): 
                if transition.is_enabled():
                    transition.fire()
                    transitions_available = True
                    break
             

        print('\nViše nije moguće izvesti niti jedan prijelaz.')
        print('Trenutno stanje mreže jest:\n{}\n'.format(self.get_M_as_string()))

        
        if self.check_net_finality():
            print('Mreža je završila u finalnom stanju u kojemu su sve značke' +
                   ' na mjestima koja nemaju izlaznih lukova.')
        else:
            print('Protok mreže je zaglavio u stanju u kojemu su značke' +
                  ' raspoređene i na mjestima koja imaju izlazne' +
                  ' lukove.')

    def check_net_finality(self):
        """
            Check if the network is in a final state.

            Returns
            -------
            is_final: bool
                True if Petri Net is in a final state, false otherwise.
        """
        for place in self.P:
            if place.M > 0 and not self.check_place_finality(place):
                return False
        return True

    def check_place_finality(self, place):
        """
            Check if a place is final (no output archs)

            Returns
            -------
            is_final: bool
                True if place is final, false otherwise.
        """
        for t in self.T:
            for input in t.inputs:
                if input.place == place:
                    return False
        return True


    def get_M_as_string(self):
        """
            Get Petri Net current state (number of tokens in each place)
            as a string.

            Returns
            -------
            M: string
                Petri Net state string.
        """
        return '\n'.join(['M({})={}'.format(p.name, p.M) for p in self.P])

    def parse_configuration(configuration):
        """
            Class method.
            Parse a configuration dictionary and return a Petri Net object.

            Parameters
            ----------
            configuration: dict
                Configuration in a dictionary form.
                (see any configuration in runner.py as an example)

            Returns
            -------
            net: PetriNet
                A Petri Net object defined in the configuration.
        """
        P = []
        for i in range(len(configuration['P'])):
            P.append(Place(configuration['P'][i], configuration['M'][i]))

        F = []
        T = []
        for t in configuration['T']:
            inputs = []
            outputs = []
            for f in configuration['F']:
                input = False
                output = False

                if f[0] == t: 
                    place = f[1] 
                    output = True 

                if f[1] == t: 
                    place = f[0] 
                    input = True 

                if input or output:
                    place = [p for p in P if p.name == place][0]
                    arch = Arch(place, f[2])
                    F.append(arch)
                    if input:
                        inputs.append(arch)
                    if output:
                        outputs.append(arch)

            T.append(Transition(t, inputs, outputs))

        return PetriNet(P, T, F, configuration['F'])

    def __str__(self):
        return 'P: {}\nT: {}\nF: {}'.format(', '.join([str(p) for p in self.P]),
                                             ', '.join([str(t) for t in self.T]),
                                             ', '.join(['({}, {}, {})'.\
                                             format(f[0], f[1], f[2]) for f \
                                             in self.arch_list]))
