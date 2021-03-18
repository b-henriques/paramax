
"""
— construction du système de parallélisme maximal : 7 points,
— exécution du système de parallélisme maximal : 7 points,
— bonus 1 : 3 points,
— bonus 2 : 3 points.
"""


class Task:
    """ Classe Tâche
    ---------------
    ---Attributs---
    ---------------
        name : le nom de la tâche, unique dans un système de tâche donné;
        reads : le domaine de lecture de la tâche;
        writes : le domaine d’écriture de la tâche;
        run : la fonction qui déterminera le comportement de la tâche;
    """

    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


class TaskSystem:
    """Classe Système de tâches
    ---------------
    ---Attributs---
    ---------------
        tasks : liste de tâches
        dic : dictionnaire des préférences de précendences
            Le dictionnaire des préférences de précédence contiendra, 
            pour chaque nom de tâche, les noms des tâches
            par lesquelles elle doit être précédée si un ordonnancement s’impose
    """

    # TODO: BONUS1 verification des entrées fournies à la procédure de construction du système de tâches
    """ 1. les noms des tâches peuvent être dupliqués, 
        2. le dictionnaire des préférences de précédence peut contenir des noms de tâches inexistantes, 
            peut ne pas être suffisamment complet pour le problème de minimisation donné, etc. 
        3.Réalisez un ensemble de vérificationsde validité des entrées, 
            en affichant des messages d’erreur détaillés."""

    def __init__(self, tasks, dic):
        self.tasks = tasks
        self.dic = dic

    # TODO : TaskSystem.getDependencies
    def getDependencies(taskName):
        """renvoie la liste des noms des tâches qui doivent s’exécuter avant taskName
        """
        pass

    # TODO : TaskSystem.run
    def run(self):
        """exécute les tâches du système en parallélisant celles qui peuvent être
        parallélisées
        """
        pass

    # TODO : identificaion des tâche interferentes
    """
     si deux tâches sont interférentes, il n’est pas possible
     de savoir en utilisant ces conditions dans quel ordre ces tâches doivent être exécutées : en
     effet, l’ordre dépendra des préférences de l’utilisateur ou de l’utilisatrice.
    """
    def getInterference(self):
        pass

    def isInterferent(task1, task2):
        """verifie si 2 taches sont interferentes en fonction des conditions de Bernstein

        return True si interference False sinon.
        2 taches sont non interferentes si E1&E2=EnsVide et E1&L2=EnsVide et L1&E2=EnsVide
        """
        #e1 et e2 sont disjoints si leur intersection est vide (E1&E2=EnsVide => E1 et E2 disjoints)
        return (task1.reads.isdisjoint(task2.writes)
                and task1.writes.isdisjoint(task2.reads)
                and task1.writes.isdisjoint(task2.writes)
                )

    # TODO : BONUS2 affichage du système de parallélisme maximal
    """
    Rajoutez à votre librairie une fonction qui permettrait d’afficher graphiquement le
    graphe de précédence du système de parallélisme maximal construit.
    """
