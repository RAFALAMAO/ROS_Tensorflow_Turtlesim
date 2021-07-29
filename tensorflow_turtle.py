#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import tensorflow as tf
import tensorflow.compat.v1 as tf_v1

# Para poder utilizar tf1, ya que tfv2 funciona con 
# tf_v1.disable_eager_execution() 

# Definiendo clases necesarias para cargar el modelo de tensorflow y crear
# la funcion para realizar la prediccion
class ModelWrapper():
	def __init__(self):
		# Store the session object from the main thread
		self.session = tf_v1.compat.v1.keras.backend.get_session()
		# Se carga el modelo guardado ya entrenado
		# La ruta debe ser completa y no relativa, ya que ROS no funciona
		# con rutas relativas
		self.model = tf_v1.keras.models.load_model('/home/aaron/noetic_ws/src/beginner_tutorials/scripts/21_ControlTensorFlow/turtleTFmodel')
		
	def predict(self, x):
		with self.session.graph.as_default():
			tf_v1.keras.backend.set_session(self.session)
			out = self.model.predict(np.array([x]))
			return out

class RosTfInterface():
    def __init__(self):
        self.wrapped_model = ModelWrapper()

# Variables de salida
x_out=0.0
y_out = 0.0
th_out=0.0
vel_msg = Twist()

# Variables de referencia
x_ref = input("Posicion en x deseada (0-11) ")
y_ref = input("Posicion en y deseada (0-11) ")
x_ref = float(x_ref)
y_ref = float(y_ref)
step = 0

#=============== Prediciendo con Red Neuronal
def red_neuronal(x):

	# Normaliza la entrada
	Xmin = np.array([ 0.0, 0.09936, -2.35619])
	Xmax_Xmin = np.array([2.0, 6.32746, 4.72226])
	x_N= (x-Xmin)/Xmax_Xmin 	

	y_N = rtf.wrapped_model.predict(x_N)[0]
	
	# Desnormaliza la salida
	Ymin = np.array([ 0.0, -1.1781])
	Ymax_Ymin = np.array([3.21341, 2.36114])
	y = y_N*Ymax_Ymin+Ymin

	print (y)
	return y

#=============== F. Turtle_callback
def turtle_cb(data0):
	global x_out
	global y_out
	global th_out
	x_out = data0.x
	y_out = data0.y
	th_out = data0.theta
	controller()

#=============== Controlador
def controller():
	global step
	# Senales de control proporcional
	e_p = np.sqrt((x_ref-x_out)**2+(y_ref-y_out)**2) # Error de posicion
	e_o = np.arctan2(y_ref-y_out,x_ref-x_out)-th_out # Error de orientacion
	if (abs(e_o)<0.05): step = 1
	if (abs(e_p)<0.1): step = 2
	E = np.array([step, e_p, e_o])
	Y = red_neuronal(E)
	if (step!=2):
		vel_msg.linear.x = abs(Y[0])
		vel_msg.angular.z = Y[1] 
	else:
		print('***************Finish************')
		vel_msg.linear.x = 0
		vel_msg.angular.z = 0
	print ("error de posicion ",e_p)
	print ("error de orientacion ",e_o) 
	velocity_publisher.publish(vel_msg)

#=============== Principal
if __name__ == '__main__':
	try:		
		rospy.init_node('Neuro_Turtle',anonymous=True)
		rtf = RosTfInterface()
		rospy.Subscriber('/turtle1/pose',Pose,turtle_cb)
		velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
		rospy.spin()
	except rospy.ROSInterruptException:
		pass

