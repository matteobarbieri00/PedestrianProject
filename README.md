# PedestrianProject
This is the code that allows to simulate pedestrian dynamics on a two-dimensional cellular automaton

# Local Map Model
The code is devided in the files:

	board.py
		Here the class Board is defined with its main features. The grid attribute of an instance of this class contains the cells in which are placed the pedestrians, simply represented by the integer numbers 1,2. The integer 0 stands instead for a void cell.
	deterministic.py
		Here the class Deterministic, daughter of the class Board, is defined. This corresponds to the deterministic sidestepping model.
	sidestepping.py
		Here the class Sidestepping, daughter of the class Board, is defined. This corresponds to the heterogeneous sidestepping model.
	The lounchable files, with the command "python3 'filename'" are:
		record_screen.py
			Here you can observe the evolution for fixed parameters, changable in the file.
		gif.py
			Generates a gif for the evolutions of passageways with different densities.
		graph.py
			Generates the graph of the flux in function of the density.
		generating_data.py, data_analysis.py
			Generates and process, respectively, the data for the non-organized lanes in function of the density.
		
# Floor Field Model 
The code is devided in the files:
    
    bosons.py
        Here the class Boson is defined with its main features.
    
    fermion.py
        Here the class Fermion is defined with its main features. The type of fermions are 0,1,2,3, where 0 stands for an empty cell, 1 stands for an eastbound pedestrian, 2 westbound, and 3 is used when the fermion is out of the passageway in the file "board.py". 

    board.py
        Here the class Board is defined, i.e. the object describing the passageway and its dynamics when carrying moving pedestrians.
    
    The lounchable files, with the command "python3 'filename'" are:
        animation_production.py
            Here one can observe the evolution of the passageway in different manners, by means of imputting a parameter from shell:
                1: you can observe the evolution for automatically varying parameters (not suggested)
            For the next ones one must set the parameters directly in the file.
                2: Whatch the passageway evolve and its order parameter
                3: Whatch the passageway evolve with its dynamic floor field
                4: Whatch the passageway evolve with both the order parameter and dynamic floor field.
        
        flux.py
            Here the gaph of the flux in function of the density is made.
