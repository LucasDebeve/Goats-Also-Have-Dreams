from random import choice, randint, shuffle
class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """

    def __init__(self, height, width, empty=False):
        """
         Constructeur d'un labyrinthe de height cellules de haut
         et de width cellules de large
         Les voisinages sont initialisés à des ensembles vides
         Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
         """
        self.height = height
        self.width = width
        if not empty:
            self.neighbors = {(i, j): set() for i in range(height)
                              for j in range(width)}
        else:
            # Initialisation des voisins
            self.neighbors = {}
            for i in range(height):
                for j in range(width):
                    self.neighbors[(i, j)] = set()
                    if i > 0:
                        self.neighbors[(i, j)].add((i-1, j))
                    if i < height-1:
                        self.neighbors[(i, j)].add((i+1, j))
                    if j > 0:
                        self.neighbors[(i, j)].add((i, j-1))
                    if j < width-1:
                        self.neighbors[(i, j)].add((i, j+1))

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0, j+1) not in self.neighbors[(0, j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,
                                  j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i+1, self.width -
                                1) not in self.neighbors[(i, self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1, j +
                                  1) not in self.neighbors[(i+1, j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def add_wall(self, c1, c2):
        """
        Ajoute un mur entre deux cellules adjacentes
        Paramètres:
            c1 (tuple), c2 (tuple): cellules adjacentes
        """
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def remove_wall(self, c1, c2):
        """
        Supprime un mur entre deux cellules adjacentes
        Paramètres:
            c1, c2 : cellules adjacentes
        """
        # on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Suppression du mur
        if c2 not in self.neighbors[c1]:
            self.neighbors[c1].add(c2)
        if c1 not in self.neighbors[c2]:
            self.neighbors[c2].add(c1)
    
    def get_walls(self):
            """
            Retourne la liste des murs du labyrinthe
            Retour:
                walls (list) : liste de couples de cellules
            
            ref = Maze(self.height, self.width, empty=True)
            walls = list(set((c1, c2) if c1 < c2 else (c2, c1)
                        for c1 in ref.neighbors.keys() for c2 in ref.neighbors[c1]))

            for c1 in self.neighbors.keys():
                for c2 in self.neighbors[c1]:
                    while (c1, c2) in walls:
                        walls.remove((c1, c2))
            return walls"""
            # Liste des murs
            L = []
            # Pour chaque cellule c1 de la grille
            for c1 in self.neighbors.keys():
                # Si la cellule c2 à droite de c1 est dans la grille et qu'elle n'est pas dans les voisins de c1
                if c1[1] < self.width-1 and (c1[0], c1[1]+1) not in self.neighbors[c1]:
                    # On ajoute le mur entre c1 et c2
                    L.append((c1, (c1[0], c1[1]+1)))
                # Si la cellule c2 en dessous de c1 est dans la grille et qu'elle n'est pas dans les voisins de c1
                if c1[0] < self.height-1 and (c1[0]+1, c1[1]) not in self.neighbors[c1]:
                    # On ajoute le mur entre c1 et c2
                    L.append((c1, (c1[0]+1, c1[1])))
            return L
    
    def fill(self):
        """
        Remplissage du labyrinthe en ajoutant des murs entre toutes les cellules
        """
        for c1 in self.neighbors.keys():
            while len(self.neighbors[c1]) > 0:
                c2 = self.neighbors[c1].pop()
                self.add_wall(c1, c2)

    def empty(self):
        """
        Vide le labyrinthe en supprimant tous les murs
        """
        for c1 in self.neighbors.keys():
            if c1[0] > 0:
                self.remove_wall(c1, (c1[0]-1, c1[1]))
            if c1[0] < self.height-1:
                self.remove_wall(c1, (c1[0]+1, c1[1]))
            if c1[1] > 0:
                self.remove_wall(c1, (c1[0], c1[1]-1))
            if c1[1] < self.width-1:
                self.remove_wall(c1, (c1[0], c1[1]+1))
    
    def get_contiguous_cells(self, c):
        """
        Retourne la liste des cellules contiguës à une cellule donnée (sans s’occuper des éventuels murs)
        Paramètre:
            c (tuple) : cellule
        Retour:
            cellules (list) : liste de cellules contiguës
        """
        cells = []
        if c[0] > 0:
            cells.append((c[0]-1, c[1]))
        if c[0] < self.height-1:
            cells.append((c[0]+1, c[1]))
        if c[1] > 0:
            cells.append((c[0], c[1]-1))
        if c[1] < self.width-1:
            cells.append((c[0], c[1]+1))
        return cells
    
    def get_reachable_cells(self, c):
        """
        Retourne la liste des cellules accessibles depuis une cellule donnée
        Paramètre:
            c : cellule
        Retour:
            liste de cellules
        """
        neighbors = self.neighbors[c]
        return [cell for cell in self.get_contiguous_cells(c) if cell in neighbors]
    
    @classmethod
    def gen_btree(cls, h, w):
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération par arbre binaire
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        m = Maze(h, w, empty=False)
        for cell in m.neighbors.keys():
            deleteChoice = []
            if (cell[0]+1, cell[1]) in m.get_contiguous_cells(cell) and (cell[0]+1, cell[1]) not in m.neighbors[cell]:
                deleteChoice.append((cell[0]+1, cell[1]))
            if (cell[0], cell[1]+1) in m.get_contiguous_cells(cell) and (cell[0], cell[1]+1) not in m.neighbors[cell]:
                deleteChoice.append((cell[0], cell[1]+1))

            if len(deleteChoice) > 0:
                toDelete = choice(deleteChoice)
                m.remove_wall(cell, toDelete)

        return m
    
    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération de Sidewinder
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération de Sidewinder
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        m = Maze(h, w, empty=False)
        for i in range(h):
            sequence = []
            for j in range(w):
                sequence.append((i, j))
                if randint(0, 1) == 0:
                    if j+1 < w:
                        m.remove_wall((i, j), (i, j+1))
                else:
                    if i+1 < h:
                        toDelete = choice(sequence)
                        m.remove_wall(toDelete, (toDelete[0]+1, toDelete[1]))
                    sequence = []
            sequence.append((i, j))
            toDelete = choice(sequence)
            if toDelete[0]+1 < h:
                m.remove_wall(toDelete, (toDelete[0]+1, toDelete[1]))
        for i in range(w-1):
            m.remove_wall((h-1, i), (h-1, i+1))
        return m
    
    @classmethod
    def gen_fusion(cls, h, w):
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération de fusion
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        m = Maze(h, w, empty=False)
        # Labeliser les cellules avec un entier de 1 à h*w-1
        labels = [[i for i in range((w*j)+1, (w*j)+w+1)] for j in range(0, h)]
        # On extrait la liste de tous les murs et on les mélange
        walls = m.get_walls()
        shuffle(walls)

        # Pour chaque mur
        for wall in walls:
            # Si les deux cellules n'ont pas le même label
            if labels[wall[0][0]][wall[0][1]] != labels[wall[1][0]][wall[1][1]]:
                # Supprimer le mur
                m.remove_wall(wall[0], wall[1])
                # Affecter le label de l'une des cellules à l'autre et à toutes celles qui ont le même label que la deuxième
                label = labels[wall[0][0]][wall[0][1]]
                for i in range(0, h):
                    for j in range(0, w):
                        if labels[i][j] == label:
                            labels[i][j] = labels[wall[1][0]][wall[1][1]]

        return m
    
    @classmethod
    def gen_exploration(cls, h, w):
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération par exploration
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        m = Maze(h, w, empty=False)
        # On choisit une cellule au hasard
        cell = (randint(0, h-1), randint(0, w-1))
        # On la marque comme visitée
        visited = [cell]
        # Mettre cette cellule dans une pile
        stack = [cell]
        # Tant que la pile n'est pas vide
        while len(stack) > 0:
            # On extrait la cellule en haut de la pile
            cell = stack.pop()
            # On initialise les voisins non visités
            notVisitedNeighbors = []
            # Si cette cellule a des voisins non visités
            for neighbor in m.get_contiguous_cells(cell):
                if neighbor not in visited:
                    notVisitedNeighbors.append(neighbor)
            if len(notVisitedNeighbors) > 0:
                # On la remet sur la pile
                stack.append(cell)
                # On choisit un voisin au hasard
                neighbor = choice(notVisitedNeighbors)
                # On supprime le mur entre la cellule et le voisin
                m.remove_wall(cell, neighbor)
                # On marque le voisin comme visité
                visited.append(neighbor)
                # On le met sur la pile
                stack.append(neighbor)
        return m
    
    @classmethod
    def gen_wilson(cls, h, w):
        """
        Génère un labyrinthe aléatoire selon l'algorithme de génération de Wilson
        Paramètres:
            h, w : dimensions du labyrinthe
        """
        m = Maze(h, w, empty=False)
        # On choisit une cellule au hasard
        cell = (randint(0, h-1), randint(0, w-1))
        # On la marque comme visitée
        visited = [cell]
        # Tant que toutes les cellules ne sont pas visitées
        while len(visited) < h*w:
            # On choisit une cellule au hasard
            cell = (randint(0, h-1), randint(0, w-1))
            while cell in visited:
                cell = (randint(0, h-1), randint(0, w-1))
            # Effectuer une marche aléatoire
            path = [cell]
            # Tant que la cellule atteinte n'est pas visitée
            while path[-1] not in visited:
                # On choisit un voisin au hasard
                goTo = choice(m.get_contiguous_cells(path[-1]))
                if goTo in path:
                    # On supprime les cellules jusqu'à la cellule atteinte
                    path = path[:path.index(goTo)+1]
                # On ajoute ce voisin à la marche
                else:
                    path.append(goTo)

            # On supprime les murs entre la cellule de départ et la cellule atteinte
            for i in range(len(path)-1):
                m.remove_wall(path[i], path[i+1])
            # On marque toutes les cellules de la marche comme visitées
            visited += path[:-1]
        return m

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height)
                       for j in range(self.width)}
        else:
            content = content | {(i, j): ' ' for i in range(
                self.height) for j in range(self.width) if (i, j) not in content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0, j)]+" ┃" if (0, j +
                                                1) not in self.neighbors[(0, j)] else " "+content[(0, j)]+"  "
        txt += " "+content[(0, self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,
                                  j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i+1, self.width -
                                1) not in self.neighbors[(i, self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1, j)]+" ┃" if (
                    i+1, j+1) not in self.neighbors[(i+1, j)] else " "+content[(i+1, j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    
    def solve_dfs(self, start, stop):
        """
        Résout un labyrinthe en utilisant l'algorithme de recherche en profondeur
        Paramètres:
            start, stop : cellules de départ et d'arrivée
        Retour:
            list : liste des cellules du chemin trouvé
        """
        # Initialisation de la pile
        pile = [start]
        # Mémoriser l'élément prédécesseur de start comme étant start
        pred = {start: set(start)}
        # Tant qu'il reste des cellules non-marqués
        while len(pred) < self.height * self.width:
            # On extrait la première cellule
            c = pile.pop()
            # Si c'est la cellule d'arrivée
            if c == stop:
                # C'est terminé on a trouvé un chemin vers la cellule d'arrivée
                break
            else:
                # Pour chaque cellule voisine de c
                for neighbor in self.get_reachable_cells(c):
                    # Si elle n'est pas marquée
                    if neighbor not in pred:
                        # La mettre dans la pile
                        pile.append(neighbor)
                        # On la marque
                        # Mémoriser son prédécesseur
                        if neighbor not in pred:
                            pred[neighbor] = c
                        else:
                            pred[neighbor] = pred[neighbor] | c
        # On reconstruit le chemin
        chemin = []
        # Initialiser c à A
        c = stop
        # Tant que c n'est pas D
        while c != start:
            # On ajoute c à la liste
            chemin.append(c)
            # On passe à son prédécesseur
            c = pred[c]
        # On ajoute la cellule de départ
        chemin.append(start)

        return chemin
    

    def solve_bfs(self, start, stop):
        """
        Résout un labyrinthe en utilisant l'algorithme de recherche en largeur
        Paramètres:
            start, stop : cellules de départ et d'arrivée
        Retour:
            list : liste des cellules du chemin trouvé
        """
        # Initialisation de la file
        file = [start]
        # Mémoriser l'élément prédécesseur de start comme étant start
        pred = {start: set(start)}
        # Tant qu'il reste des cellules non-marqués
        while len(pred) < self.height * self.width:
            # On extrait la première cellule
            c = file.pop(0)
            # Si c'est la cellule d'arrivée
            if c == stop:
                # C'est terminé on a trouvé un chemin vers la cellule d'arrivée
                break
            else:
                # Pour chaque cellule voisine de c
                for neighbor in self.get_reachable_cells(c):
                    # Si elle n'est pas marquée
                    if neighbor not in pred:
                        # La mettre dans la file
                        file.append(neighbor)
                        # On la marque
                        # Mémoriser son prédécesseur
                        if neighbor not in pred:
                            pred[neighbor] = c
                        else:
                            pred[neighbor] = pred[neighbor] | c
        # On reconstruit le chemin
        chemin = []
        # Initialiser c à A
        c = stop
        # Tant que c n'est pas D
        while c != start:
            # On ajoute c à la liste
            chemin.append(c)
            # On passe à son prédécesseur
            c = pred[c]
        # On ajoute la cellule de départ
        chemin.append(start)

        return chemin