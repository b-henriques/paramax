from graphviz import Digraph
from threading import Event, Thread
from time import sleep
from random import randint

#==========================================================================================
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
#===========================================================================================

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

    def __init__(self, tasks, dic):
        self.tasks = tasks
        self.dic = dic
        self.makeGraph()

    def getDependencies(self, taskName):
        """renvoie la liste des noms des tâches qui doivent s’exécuter avant taskName
        """
        # s = sommet dont la tache est taskName
        s = self.graph[taskName]
        # on cherche tous les sommets qui le precedent
        prec = []
        prec = s.getDependenciesRec(prec)
        # on elimine les doublons
        ensemble = set()
        for p in prec:
            ensemble.add(p.task.name)
        # on transorme le set en liste
        prec = list(ensemble)
        return prec

          # TODO: BONUS1 verification des entrées fournies à la procédure de construction du système de tâches
    """ 1. les noms des tâches peuvent être dupliqués,
        2. le dictionnaire des préférences de précédence peut contenir des noms de tâches inexistantes,
            peut ne pas être suffisamment complet pour le problème de minimisation donné, etc.
        3.Réalisez un ensemble de vérificationsde validité des entrées,
            en affichant des messages d’erreur détaillés."""

    # TODO : TaskSystem.run + tests

    def taskRun(sommet):
        # ecoute tous les events des taches qui le precedent directement
        for e in sommet.events:
            e.wait()
        #sleep(randint(1,10))
        # toutes les taches qui le precedent ont termine, il peut s'executer
        sommet.task.run()
        #print(sommet.task.name)
        # declenhe son event s'il y en a, càd s'il precede d'autres taches
        if sommet.event:
            sommet.event.set()

    def run(self):
        """exécute les tâches du système en parallélisant celles qui peuvent être
        parallélisées
        """
        for s in self.graph.values():
            if len(s.sortants): # cette tache precede d'autres taches
                s.event = Event() # on lui attribue un event
                for s_fils in s.sortants: # toutes les taches qui sont directement precedees par cette tache, ecouteront cet event
                    s_fils.events.append(s.event)
        # on lance toutes les taches en parallele, les precedences sont verifies par les events
        for s in self.graph.values():
            Thread(target=TaskSystem.taskRun, args=[s]).start()

    # ==========================================================================================================
    class Sommet:
        """classe Sommet
        ---------------
        ---Attributs---
        ---------------
            task_name : nom de la tache qu'il represente
            entrants : soit ce sommet u, entrants = t tq (t,u) existe càd sommets qui on une fleche vers ce sommet
            sortants : voisinage de ce sommet, sortants = v tq (u,v) existe
            sommets_accessibles : les sommets accessibles depuis ce sommet
            events : les evnts qu'il faut attendre pour commencer la tache
        """

        # TODO: changer sommets_accessibles par une recherche en profondeur
        def __init__(self, task):
            self.task = task
            self.entrants = []
            self.sortants = []
            self.sommets_accessibles = []
            self.event = None
            self.events = []

        def accessibleUpdate(self, sommet):
            """actualise sommet_accessibles des sommets entrants lors d'un ajout d'une arete au graph 
            """
            self.sommets_accessibles.append(sommet)
            if not self.entrants:
                for s in self.entrants:
                    s.accessibleUpdate(sommet)

        def getDependenciesRec(self, prec):
            """renvoi tous les sommets qui precedent sommet
            """
            prec.extend(self.entrants)
            for s in self.entrants:
                prec.extend(s.getDependenciesRec(prec))
            return prec

    # =============================================================================================================

    def initGraph(self):
        """initialise le graph

        1 sommet = 1 tache
        """
        self.graph = {}
        for t in self.tasks:
            self.graph[t.name] = TaskSystem.Sommet(t)

    def ajout(self, t1, t2):
        """on ajoute l'arete (t1,t2) au graph si cela ne crée pas de cycle, ou si on n'a pas encore cette precedence par transitivité
        """
        sommetU = self.graph[t1.name]
        sommetV = self.graph[t2.name]
        # chemin de v à u ?
        # oui => ajout de (u,v) cree un cycle donc erreur
        if sommetU in sommetV.sommets_accessibles:
            return False
        else:  # non => chemin u à v?
            # si chemin alors on a déjà la précédence par transitivité
            # sinon:
            if sommetV not in sommetU.sommets_accessibles:
                # ajout u -> v
                sommetU.sortants.append(sommetV)
                sommetV.entrants.append(sommetU)
                # v est accessible depuis u et par conséquent tous les sommets qui précèdent u
                # on met a jour les sommets accessibles
                sommetU.sommets_accessibles.extend(sommetV.sommets_accessibles)
                sommetU.accessibleUpdate(sommetV)
            return True

    # TODO : ajouter param type qui donne le type de erreur, cyle explicite, cycle implicite, pas de preference communiquee(pas de transitivite)
    def messageErreurPrecedence(t1, t2):
        raise Exception(
            "Impossible d'établir une relation de précédence entre %s et %s. Veuillez vérifier vos préférences de précédence." % (t1.name, t2.name))


    """
    si deux tâches sont interférentes, il n’est pas possible
    de savoir en utilisant ces conditions dans quel ordre ces tâches doivent être exécutées : en
    effet, l’ordre dépendra des préférences de l’utilisateur ou de l’utilisatrice.
    """
    def makeGraph(self):
        """construit le graph de precedence du systeme de parallelisme maximal
        """
        self.initGraph()
        interferences = self.getInterferences()
        aTraiter = []
        # e de la forme (t1,t2) (interference tache t1 et tache t2)
        for e in interferences:
            # on verifie les preferences de precedence
            t1 = e[0]
            t2 = e[1]
            # si t1 precede t2
            if (t1.name in self.dic[t2.name]):
                # si t2 precede t1 aussi alors erreur
                if(t2.name in self.dic[t1.name]):
                    TaskSystem.messageErreurPrecedence(t1, t2)
                else:  # t2 ne precede pas t1 dans les préférences
                    if not self.ajout(t1, t2):
                        TaskSystem.messageErreurPrecedence(t1, t2)
            elif (t2.name in self.dic[t1.name]):  # si t2 precede t1
                if not self.ajout(t2, t1):
                    TaskSystem.messageErreurPrecedence(t1, t2)
            else:  # aucune preference à été communiquée explicitement
                # on garde les taches à part
                aTraiter.append(e)
        for a in aTraiter:
            t1 = a[0]
            t2 = a[1]
            if not self.ajout(t1, t2):  # si on ne peut pas ajouter (t1,t2)
                # peut on ajouter (t2,t1)?
                # si non alors on ne dispose pas de preferences suffisantes pour creer le systeme
                if not self.ajout(t2, t1):
                    TaskSystem.messageErreurPrecedence(t1, t2)

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
        for e1 in l1:
            if e1 in l2:
                return False
        return True

    def isInterferent(task1, task2):
        """verifie si 2 taches sont interferentes en fonction des conditions de Bernstein

        return True si interference False sinon.
        2 taches sont non interferentes si E1&E2=EnsVide et E1&L2=EnsVide et L1&E2=EnsVide
        """
        # e1 et e2 sont disjoints si leur intersection est vide (E1&E2=EnsVide => E1 et E2 disjoints)
        return not(TaskSystem.estDisjoint(task1.reads, task2.writes)
                   and TaskSystem.estDisjoint(task1.writes, task2.reads)
                   and TaskSystem.estDisjoint(task1.writes, task2.writes)
                   )

    # BONUS2 affichage du système de parallélisme maximal
    # utilisation graphviz https://pypi.org/project/graphviz/

    def draw(self):
        """permet d'afficher graphiquement le graphe de précédence du système de parallélisme maximal construit
        le fichier .pdf est placé dans le directoire Graphs
        """
        systeme = Digraph()
        # pour ajoute chaque sommet du systeme au graphe et on ajoute aussi chaque arete (sortant de ce sommet)
        for sommet in self.graph.values():
            systeme.node(sommet.task.name, label=sommet.task.name)
            for s in sommet.sortants:
                systeme.edge(sommet.task.name, s.task.name)
        systeme.render('Graphs/GrapheTaskSystem', view=True)


##########################################################
X = None
Y = None
Z = None


def runT1():
    global X
    print("running t1")
    X = 1


def runT2():
    global Y
    print("running t2")
    Y = 2


def runTsomme():
    global X, Y, Z
    print("running tsomme")
    Z = X+Y
    print(Z)


t1 = Task("T1", [], ["X"], runT1)
t2 = Task("T2", [], ["Y"], runT2)
tsomme = Task("Tsomme", ["Y", "X"], ["Z"], runTsomme)
tasksystem = TaskSystem([t1, t2, tsomme], {"T1": [], "T2": [
                        "T1"], "Tsomme": ["T1", "T2"]})
#print(tasksystem.getDependencies("Tsomme"))
tasksystem.draw()
tasksystem.run()

"""
t1 = Task("T1", [], ["X1", "X2"], None)
t2 = Task("T2", [], ["Y1", "Y2"], None)
t3 = Task("T3", ["X2", "Y2"], [], None)
t4 = Task("T4", ["X1", "Y2"], [], None)
t5 = Task("T5", ["Y1", "Y2"], [], None)
t6 = Task("T6", [], [], None)
tasksystem = TaskSystem([t1, t2, t3, t4, t5, t6],
                        {"T1": [], "T2": [], "T3": ["T1", "T2"], "T4": ["T1", "T2"], "T5": [], "T6": []})
#print(tasksystem.getInterferences())
#print(tasksystem.getDependencies("T4"))
tasksystem.draw()
#tasksystem.run()
"""


"""
t1 = Task("T1", [], ["X", "Y"], None)
t2 = Task("T2", ["X"], ["Z"], None)
t3 = Task("T3", ["X", "Z"], [], None)
tasksystem = TaskSystem([t1, t2, t3],
                        {"T1": ["T3"], "T2": ["T1"], "T3": ["T2"]})
print(tasksystem.getInterferences())
print(tasksystem.getDependencies("T3"))
tasksystem.draw()
"""
