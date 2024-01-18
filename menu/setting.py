from config.config import HD, FHD, QHD, UHD, RUHD, INIT_WIDTH, INIT_HEIGHT
import numpy as np

screens = [(INIT_WIDTH, INIT_HEIGHT), HD, FHD, QHD, UHD, RUHD, 'Full Screen']

levels = np.arange(1, 7.1, 0.25).tolist()
