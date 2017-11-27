import pygame
# http://www.raywenderlich.com/4946/introduction-to-a-pathfinding


class GridWorld():
    """ Grid world that contains Pauls (and other things) living in cells. """
    def __init__(self, width=10, height=10, cell_size=50):
        pygame.init()
        screen_size = (height*cell_size, width*cell_size)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption = ('Paul World')
        self.actors = {}
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self._init_cells()
        self._init_paul_and_cake()
        self.add_tile_type = None

    def _draw_background(self):
        WHITE = (255, 255, 255)
        self.screen.fill(WHITE)

    def _init_cells(self):
        self.cells = {}
        cell_size = (self.cell_size, self.cell_size)
        for i in range(self.height):
            for j in range(self.width):
                cell_coord = (i*self.cell_size, j*self.cell_size)
                self.cells[(i, j)] = Cell(self.screen, cell_coord, cell_size)

    def _add_coords(self, a, b):
        """ Returns a third coord that is equivalent to
            (a[0]+b[0], a[1]+b[1]) """
        return tuple(map(sum, zip(a, b)))

    def _init_paul_and_cake(self):
        self.paul = Paul((0, 0), self, './images/paul.jpg')
        self.cake = Actor((9, 9), self, './images/cake.jpg',
                          removable=False, is_obstacle=False)
        self.actors[(0, 0)] = self.paul
        self.actors[(9, 9)] = self.cake

    def _draw_cells(self):
        all_cells = self.cells.values()
        for cell in all_cells:
            cell.draw()

    def _draw_actors(self):
        all_actors = self.actors.values()
        for actor in all_actors:
            actor.draw()

    def _redraw(self):
        self._draw_background()
        self._draw_actors()
        self._draw_cells()
        pygame.display.update()

    def _is_in_grid(self, cell_coord):
        """ tells us whether cell_coord is valid and in range of the actual
            grid dimensions """
        valid_x = (-1 < cell_coord[0] < self.width)
        valid_y = (-1 < cell_coord[1] < self.height)
        return valid_x and valid_y

    def _is_occupied(self, cell_coord):
        try:
            actor = self.actors[cell_coord]
            return actor.is_obstacle
        except:
            return False

    def _add_swamp(self, mouse_pos):
        """ Adds a swamp tile in the cell that mouse_pos indicates """
        swamp_coord = (mouse_pos[0]//50, mouse_pos[1]//50)
        if self._is_occupied(swamp_coord):
            if self.actors[swamp_coord].removable:
                self.actors.pop(swamp_coord, None)
        elif swamp_coord != self.cake.cell_coordinates:
            swamp = ObstacleTile(swamp_coord, self, './images/swamp.jpg',
                                is_unpassable=False, terrain_cost=3)
            self.actors[swamp_coord] = swamp

    def _add_lava(self, mouse_pos):
        """ Adds a lava tile in the cell that mouse_pos indicates """
        lava_coord = (mouse_pos[0]//50, mouse_pos[1]//50)
        if self._is_occupied(lava_coord):
            if self.actors[lava_coord].removable:
                self.actors.pop(lava_coord, None)
        elif lava_coord != self.cake.cell_coordinates:
            lava = ObstacleTile(lava_coord, self, './images/lava.jpg',
                                is_unpassable=True, terrain_cost=0)
            self.actors[lava_coord] = lava

    def get_terrain_cost(self, cell_coord):
        try:
            actor = self.actors[cell_coord]
            if actor.terrain_cost is not None:
                return actor.terrain_cost
            else:
                return 0
        except:
            return 0

    def main_loop(self):
        """ Updates graphics and checks for pygame events """
        running = True
        while (running):
            self._redraw()
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    if self.add_tile_type == 'lava':
                        self._add_lava(event.pos)
                    elif self.add_tile_type == 'swamp':
                        self._add_swamp(event.pos)
                elif event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paul.run_astar(self.cake.cell_coordinates, self)
                        self.paul.get_path()
                    elif event.key == pygame.K_l:
                        self.add_tile_type = 'lava'
                    elif event.key == pygame.K_s:
                        self.add_tile_type = 'swamp'


class Actor(object):
    def __init__(self, cell_coordinates, world, image_loc,
                 removable=True, is_obstacle=True):
        self.is_obstacle = is_obstacle
        self.removable = removable
        """ takes coordinates as a tuple """
        if world._is_occupied(cell_coordinates):
            raise Exception('%s is already occupied!' % cell_coordinates)
        self.cell_coordinates = cell_coordinates
        self.world = world
        self.image = pygame.image.load(image_loc)
        self.image_rect = self.image.get_rect()

    def draw(self):
        cells = self.world.cells
        cell = cells[self.cell_coordinates]
        # add an offset so that the image will fit inside the cell border.
        x_y_coords = self.world._add_coords(cell.coordinates, (3, 3))
        rect_dim = (self.image_rect.width, self.image_rect.height)
        self.image_rect = pygame.Rect(x_y_coords, rect_dim)
        screen = self.world.screen
        screen.blit(self.image, self.image_rect)


class ObstacleTile(Actor):
    def __init__(self, cell_coordinates, world, image_loc,
                 terrain_cost=0, is_unpassable=True):
        super(ObstacleTile, self) \
            .__init__(cell_coordinates, world, image_loc, removable=True,
                      is_obstacle=is_unpassable)
        self.terrain_cost = terrain_cost


class Cell():
    def __init__(self, draw_screen, coordinates, dimensions):
        self.draw_screen = draw_screen
        self.coordinates = coordinates
        self.dimensions = dimensions
        self.color = (0, 0, 0)
        self.g_cost = None
        self.h_cost = None

    @property
    def f_cost(self):
        if self.g_cost is None or self.h_cost is None:
            return None
        return self.g_cost + self.h_cost

    def draw(self):
        COST_TO_DRAW = ''
        # COST_TO_DRAW = self.g_cost
        # COST_TO_DRAW = self.h_cost
        COST_TO_DRAW = self.f_cost
        line_width = 2
        rect = pygame.Rect(self.coordinates, self.dimensions)
        pygame.draw.rect(self.draw_screen, self.color, rect, line_width)
        font = pygame.font.Font(None, 20)
        text = font.render(' '+str(COST_TO_DRAW), 1, (10, 10, 10))
        self.draw_screen.blit(text, self.coordinates)


class Paul(Actor):
    def __init__(self, init_coordinates, world, image_loc):
        super(Paul, self) \
            .__init__(init_coordinates, world, image_loc, removable=False)
        self.cells = world.cells
        self.open_list = []
        self.closed_list = []

    def get_h_cost(self, coord_a, coord_b):
        """ returns the h score, the manhattan distance between coord_a and
            the coord_b. """
        return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])

    def get_open_adj_coords(self, coords):
        """ returns list of valid coords that are adjacent to the argument,
            open, and not in the closed list. """
        # modify directions and costs as needed
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        diagonal = [(1,1), (1,-1), (-1,1), (-1,-1)]
        hops = [(2, 0), (0, 2), (-2, 0), (0, -2)]

        all_adj = [self.world._add_coords(coords, d) for d in directions]
        all_adj_diagonal = [self.world._add_coords(coords, d) for d in diagonal]
        all_adj_hops = [self.world._add_coords(coords, d) for d in hops]

        in_bounds = [self.is_valid(c) for c in all_adj]
        in_bounds_diagonal = [self.is_valid(c) for c in all_adj_diagonal]
        in_bounds_hops = [self.is_valid(c) for c in all_adj_hops]

        costs = []
        open_adj = []
        for i, coord in enumerate(all_adj):
            if(in_bounds[i]):
                costs.append(1 + self.world.get_terrain_cost(coord))
                open_adj.append(coord)

        for i, coord in enumerate(all_adj_diagonal):
            if(in_bounds_diagonal[i]):
                costs.append(3 + self.world.get_terrain_cost(coord))
                open_adj.append(coord)

        for i, coord in enumerate(all_adj_hops):
            if(in_bounds_hops[i]):
                costs.append(8 + self.world.get_terrain_cost(coord))
                open_adj.append(coord)

        return open_adj, costs

    def is_valid(self, coord):
        return self.world._is_in_grid(coord) \
            and not self.world._is_occupied(coord) \
            and coord not in self.closed_list

    def get_lowest_cost_open_coord(self):
        open_cells = self.open_list
        sorted_cells = sorted(open_cells, key=lambda s: self.cells[s].f_cost)
        return sorted_cells[0]

    def reset_cell_values(self):
        self.destination_coord = None
        for cell in self.cells.values():
            cell.color = (0, 0, 0)
            cell.parents_coords = None
            cell.g_cost = None
            cell.h_cost = None

    def get_path(self):
        """ Follows cell parents backwards until the initial cell is reached to
            create a path, which is the list of coordinates that paul will
            travel through to reach the destination. """
        coord_list = [self.destination_coord]
        print("final cost is {}".format(self.cells[coord_list[-1]].f_cost))
        while self.start_coord not in coord_list:
            try:
                coord_list.append(self.cells[coord_list[-1]].parents_coords)
            except:
                print('No path found to destination coord!')
                break
        for coord in coord_list:
            if coord is not None:
                self.cells[coord].color = (0, 255, 0)
        return coord_list

    def run_astar(self, destination_coord, world):
        """ Updates cells g,h,f, and parent coordinates until the destination
            square is found. """
        self.reset_cell_values()
        self.open_list = []
        self.closed_list = []
        self.start_coord = self.cell_coordinates
        self.destination_coord = destination_coord
        coord_s = self.cell_coordinates
        cell_s = self.cells[coord_s]
        cell_s.g_cost = 0
        cell_s.h_cost = self.get_h_cost(coord_s, destination_coord)
        self.open_list = [coord_s]
        while len(self.open_list) > 0:
            coord_s = self.get_lowest_cost_open_coord()
            cell_s = self.cells[coord_s]
            self.open_list.remove(coord_s)
            self.closed_list.append(coord_s)
            walkable_open_coords, costs = self.get_open_adj_coords(coord_s)
            for idx, coord in enumerate(walkable_open_coords):
                cell = self.cells[coord]
                g_cost = cell_s.g_cost + costs[idx]
                h_cost = self.get_h_cost(coord, destination_coord)
                f_cost = g_cost + h_cost
                if coord in self.open_list:
                    old_f_cost = cell.f_cost
                    if f_cost < old_f_cost:
                        cell.g_cost = g_cost
                        cell.h_cost = h_cost
                        cell.parents_coords = coord_s
                else:
                    self.open_list.append(coord)
                    cell.g_cost = g_cost
                    cell.h_cost = h_cost
                    cell.parents_coords = coord_s


if __name__ == "__main__":
    g = GridWorld()
    g.main_loop()
