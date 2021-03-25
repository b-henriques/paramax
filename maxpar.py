
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

    # TODO : identificaion des tâche interferentes et relation de precedence
    """
     si deux tâches sont interférentes, il n’est pas possible
     de savoir en utilisant ces conditions dans quel ordre ces tâches doivent être exécutées : en
     effet, l’ordre dépendra des préférences de l’utilisateur ou de l’utilisatrice.
    """

    def makePrecedence(self):
        interferences = self.getInterferences
        precedences = {}
        for e in interferences:
            # on verifie les preferences de precedence
            # si t1 precede t2
            t1 = e[1]
            t2 = e[2]
            if (t1.name in self.dic[t2.name]):
                # si t2 precede t1 aussi alors erreur
                if(t2.name in self.dic[t1.name]):
                    raise Exception(
                        "Impossible d'établir une relation de précédence entre %s et %s . \n Veuillez vérifier vos préférences de précédence")
                else:  # on verifie si la tache qui doit etre precedée est dejà dans le dictionnaire precedences
                    p = precedences.get(t1)
                    # si non alors on ajoute une entree qui a comme cle la tache precedée et comme valeur [tachequiprécède]
                    if p == None:
                        precedences[t1] = [t2]
                    else:  # si oui alors on ajoute la tache qui precède à la valeur de la tache precedée
                        p.append(t2)

            # si t2 precede t1

            # on verifie si la tache qui doit etre precedée est dejà dans le dictionnaire precedences

            # si non alors on ajoute une entree qui a comme cle la tache precedée et comme valeur [tachequiprécède]

            # si oui alors on ajoute la tache qui precède à la valeur de la tache precedée
            pass

    def getInterferences(self):
        """retourne les interferences entre les taches
        sous la forme d'une liste de tuples (T1, T2)
        """
        # la liste à retourner
        interferences = []
        # calcul combinatoire, 2 parmi n taches
        for i in range(0, len(self.tasks)):
            for j in range(i+1, len(self.tasks)):
                t1 = self.tasks[i]
                t2 = self.tasks[j]
                # si t1 et t2 interferents on ajoute le tuple (t1,t2) à interferences
                if(TaskSystem.isInterferent(t1, t2)):
                    interferences.append((t1, t2))
        return interferences

    def estDisjoint(l1, l2):
        """retourne vrai si l1 et l2 sont disjoints, faux sinon
        """
        # si un element est dans l1 et l2 alors l1 et l2 ne sont pas disjoints
        for e in (l1 & l2):
            return False
        return True

    def isInterferent(task1, task2):
        """verifie si 2 taches sont interferentes en fonction des conditions de Bernstein

        return True si interference False sinon.
        2 taches sont non interferentes si E1&E2=EnsVide et E1&L2=EnsVide et L1&E2=EnsVide
        """
        # e1 et e2 sont disjoints si leur intersection est vide (E1&E2=EnsVide => E1 et E2 disjoints)
        return (TaskSystem.estDisjoint(task1.reads, task2.writes)
                and TaskSystem.estDisjoint(task1.writes, task2.reads)
                and TaskSystem.estDisjoint(task1.writes, task2.writes)
                )
        # reads et writes comme liste dans l'ennonce => passage vers set? apres verification des entrées fournies

    # TODO : BONUS2 affichage du système de parallélisme maximal
    # utilisation graphviz https://pypi.org/project/graphviz/
    """
    Rajoutez à votre librairie une fonction qui permettrait d’afficher graphiquement le
    graphe de précédence du système de parallélisme maximal construit.
    """


dic = {'t': ['1', '2']}
p = dic.get('t')
print(p)
p.append('3')
print(p)