import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import matplotlib

class Renderer:
    def __init__(self,world_size=30):
        matplotlib.rcParams['toolbar'] = 'None'
        self.fig,self.ax=plt.subplots(figsize=(10,8))
        self.world_size=world_size
        plt.ion() #interactive mode - updates live

    def draw(self,car,lot=None,title=""):
        self.ax.clear()

        #world bounds
        self.ax.set_xlim(0,32)
        self.ax.set_ylim(4,18)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#e8e8e8')
        self.ax.grid(True,alpha=0.3)


        #draw parking space if provided
        if lot is not None:
            #draw curb
            self.ax.axhline(y=lot.curb_y,color='#555', linewidth=3,label='curb')

            #draw road surface above curb
            road = patches.Rectangle(
                (-2,lot.curb_y),self.world_size+4,self.world_size,
                facecolor='#b0bec5',alpha=0.3
            )
            self.ax.add_patch(road)
            
            #draw parkin space
            px , py , pw , ph = lot.get_parking_space()
            space = patches.Rectangle(
                (px, py), pw , ph ,
                linewidth=2, edgecolor='white',
                facecolor='#c8e6c9' , alpha=0.8,
                linestyle='--'
            )
            self.ax.add_patch(space)
            self.ax.text(px + pw/2, py +ph/2,'TARGET',
                         ha='center', va='center',
                         fontsize=7,color='#2e7d32',fontweight='bold')
            
            #draw obstacles cars (grey)
            for (ox , oy ,ow ,oh) in lot.obstacles:
                obs = patches.Rectangle(
                    (ox , oy) ,ow ,oh,
                    facecolor='#607d8b' , edgecolor='#37474f',
                    linewidth=1.5,alpha=0.9
                )
                self.ax.add_patch(obs)

            # distance indicator
            dist = lot.distance_to_target(car)
            parked = lot.is_parked(car)
            collision = lot.is_collision(car)
            if parked:
                status = "PARKED! "
                color = "green"
            elif collision:
                status = "COLLISION! "
                color = "red"
            else:
                status = f"dist: {dist:.2f}m"
                color = "black"
            self.ax.set_xlabel(f'X (meters) - status: {status}', color=color)

        #draw ego car body
        corners = car.get_corners()
        car_shape = Polygon(corners,closed=True,
                            facecolor='#1565c0',edgecolor='#0d47a1',
                            linewidth=1.5,alpha=0.9)
        self.ax.add_patch(car_shape)
        if parked:
            self.ax.text(
                0.5, 0.5, 'PARKED!',
                transform=self.ax.transAxes,
                fontsize=24, fontweight='bold',
                color='green', alpha=0.8,
                ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5)
            )
        elif collision:
            self.ax.text(
                0.5, 0.5, 'OOPS!',
                transform=self.ax.transAxes,
                fontsize=24, fontweight='bold',
                color='red', alpha=0.8,
                ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5)
    )

        #draw a small arrow showing heading direction
        arrow_len =1.2
        self.ax.annotate('',
                         xy=(car.x+arrow_len*np.cos(car.heading),
                             car.y + arrow_len*np.sin(car.heading)),
                             xytext=(car.x,car.y),
                             arrowprops=dict(arrowstyle='->',color='yellow',lw=2))
        #draw a dot at car center
        self.ax.plot(car.x,car.y,'yo',markersize=4)

        if title:
            self.ax.set_title(f"{title}  |  car y={car.y:.2f}", fontsize=10)
        
        
        self.ax.set_ylabel('Y (meters)')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.005)

    def close(self):
        plt.ioff()
        plt.close()
            