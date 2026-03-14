import gymnasium as gym
import pygame
import cv2 

# Initialise the environment
env = gym.make("LunarLander-v3", render_mode="rgb_array")

# Reset the environment to generate the first observation
observation, info = env.reset(seed=42)
for _ in range(200):
    # this is where you would insert your policy
    action = env.action_space.sample()

    # step (transition) through the environment with the action
    # receiving the next observation, reward and if the episode has terminated or truncated
    observation, reward, terminated, truncated, info = env.step(action)
    r = env.render()
    surface = pygame.surfarray.make_surface(r)
    surface = pygame.transform.rotate(surface, 270)
    surface = pygame.transform.flip(surface, True, False)
    pygame.image.save(surface, 'pic/gtest.png')

    frame_bgr = cv2.cvtColor(r, cv2.COLOR_RGB2BGR)
    cv2.imshow('', frame_bgr)
    cv2.waitKey(1)
    # If the episode has ended then we can reset to start a new episode
    if terminated or truncated:
        observation, info = env.reset()

env.close()
cv2.destroyAllWindows()
