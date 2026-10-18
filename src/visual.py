import pygame
from .models import Hub, Connections, Drone

Margin = 100
width_page = 1280
height_page = 720


def proportions(zones: dict[str, Hub]) -> tuple[float, float, float, float]:
    """General function of proportions and margins of screen."""
    min_x: float = float("inf")
    max_x: float = float("-inf")
    min_y: float = float("inf")
    max_y: float = float("-inf")
    for i in zones:
        if min_x > zones[i].pos_x:
            min_x = zones[i].pos_x
        if max_x < zones[i].pos_x:
            max_x = zones[i].pos_x
        if min_y > zones[i].pos_y:
            min_y = zones[i].pos_y
        if max_y < zones[i].pos_y:
            max_y = zones[i].pos_y
    width = max_x - min_x
    height = max_y - min_y
    if height == 0:
        height = height_page / 2
    if width == 0:
        width = width_page / 2
    prop_x = (width_page - (2 * Margin)) / width
    prop_y = (height_page - (2 * Margin)) / height
    return prop_x, prop_y, min_x, min_y


def running(zones: dict[str, Hub], connections: dict[str, list[Connections]],
            drones_lists: list[Drone], start: Hub, end: Hub,
            total_moves: int) -> None:
    """Visual representation of the loop.

    Simulates it with position and proportion using the pygame library.
    """
    pygame.init()
    screen = pygame.display.set_mode((width_page, height_page))
    pygame.display.set_caption("Fly In")
    a = pygame.image.load("src/Img/icon.png")
    test_obj = pygame.image.load(
        "src/Img/drone.png").convert_alpha()
    drone = pygame.transform.scale_by(test_obj, (0.09, 0.09))
    pygame.display.set_icon(a)
    clock = pygame.time.Clock()
    running = True
    prop_x, prop_y, min_x, min_y = proportions(zones)
    turn = 0
    font = pygame.font.SysFont(None, 20)
    while running:
        positions = [""]
        screen.fill("black")
        for i in zones:
            colour = zones[i].color
            if colour is None:
                colour = "black"
            if colour == "rainbow":
                colour = "pink"
            r = pygame.Rect(0, 0, 40, 40)
            r.center = (
                ((zones[i].pos_x - min_x) * prop_x + Margin,
                 (zones[i].pos_y - min_y) * prop_y + Margin))
            pygame.draw.rect(screen, colour, r)
        for f in drones_lists:
            if len(f.path) - 1 <= turn:
                r = drone.get_rect(center=(
                    (zones[end.name].pos_x - min_x) * prop_x + Margin,
                    (zones[end.name].pos_y - min_y) * prop_y + Margin))
                screen.blit(drone, r)
                continue
            else:
                k = f.path[turn].split("-")
                r = drone.get_rect(center=(
                    (zones[k[0]].pos_x - min_x) * prop_x + Margin,
                    (zones[k[0]].pos_y - min_y) * prop_y + Margin))
                screen.blit(drone, r)
                if (f.path[turn] != start.name and f.path[turn] != end.name
                        and f.path[turn - 1] != f.path[turn]):
                    positions.append(f"D{f.id_drone}-{f.path[turn]} ")
        moves = font.render(f"{str(turn)}", True, "white")
        y = 10
        for pos in positions:
            txt = font.render(f"{pos}", True, "white")
            screen.blit(txt, (10, y))
            y = y + 10
        screen.blit(moves, (30, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if turn >= total_moves:
            running = False
            return
        turn += 1
        pygame.display.flip()
        clock.tick(1)

    pygame.quit()
