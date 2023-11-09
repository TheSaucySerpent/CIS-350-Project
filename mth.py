# Import the NetworkX library
import networkx as nx

# Import matplotlib for graph visualization
import matplotlib.pyplot as plt

# Create an empty graph object
G = nx.Graph()

a = {"a" : 0 ,  "b" :  25 , "c" : 17 , "d" : 34 , "e" : 19}
b = {"a" : 25 , "b" :  0 ,  "c" : 23 , "d" : 18 , "e" : 31}
c = {"a" : 17 , "b" :  23 , "c" : 0 ,  "d" : 24 , "e" : 16}
d = {"a" : 34 , "b" :  18 , "c" : 24 , "d" : 0 ,  "e" : 29}
e = {"a" : 19 , "b" :  31 , "c" : 16 , "d" : 29 , "e" : 0}

li = [a,b,c,d,e]

def get_smallest_value(d):
    # Remove keys with value 0 and find the minimum among the rest
    return min(val for val in d.values() if val != 0)

# Finding smallest value in each dictionary
min_a = get_smallest_value(a)
min_b = get_smallest_value(b)
min_c = get_smallest_value(c)
min_d = get_smallest_value(d)
min_e = get_smallest_value(e)

print("Smallest value in 'a':", min_a)
print("Smallest value in 'b':", min_b)
print("Smallest value in 'c':", min_c)
print("Smallest value in 'd':", min_d)
print("Smallest value in 'e':", min_e)







# Draw the tree
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, font_size=18)

# Show the plot
#plt.show()


        """if keys[pygame.K_r]:
            mc.gun.reload()
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - mc.last_dodge > 1000:
                mc.move(keys, 150, True)
                mc.last_dodge = current_time + 100
            else:
                mc.move(keys, 0)
        else:
            mc.move(keys, 0)

        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if mc.gun != 0:
                mc.gun.attack()
            else:
                print("You don't got a gun!")

        # Check for collisions between character and enemies
        for enemy in enemies:
            enemy.move_towards_character()
            if mc.x < enemy.x + enemy.width - 10 and mc.x + mc.width > enemy.x \
                    and mc.y < enemy.y + enemy.height - 10 and mc.y + mc.height > enemy.y:
                # Characters are colliding, character takes damage
                mc.take_damage(10)



    # Draw projectiles
    for g in glob_var.guns:
        for p in g.projectiles:
            p.move()
            pygame.draw.rect(screen, (255, 255, 0), (p.x, p.y, p.width, p.height))
        g.update_projectiles()

    # Draw/kill the enemy
    for enemy in enemies:
        if enemy.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.width, enemy.height))
        else:
            enemies.remove(enemy)

    # Draw objects
    for ob in glob_var.objs:
        pygame.draw.rect(screen, (0, 255, 0), (ob.x, ob.y, ob.width, ob.height))

    pygame.draw.rect(screen, (0, 0, 255), (mc.x, mc.y, mc.width, mc.height))

    # Display the character's stats
    health_text = font.render(f"Health: {mc.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    ammo_text = font.render(f"Ammo: {mc.gun.mag_ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 30))
    mag_text = font.render(f"Mags: {mc.gun.mag_count}", True, (255, 255, 255))
    screen.blit(mag_text, (10, 50))
"""
