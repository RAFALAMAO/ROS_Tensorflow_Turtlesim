# ROS_Tensorflow_Turtlesim
En este GIT solo se da el ejemplo para poder integrar Tensorflow en un nodo de ROS para predecir desde un modelo ya entrenado

# Requerimientos
1. ROS Noetic (con algunos ajustes puede funcionar en otras versiones de ROS)
2. TensorFlow v2 (con algunos ajustes puede funcionar en otras versiones de ROS)

# Notas
1. La carpeta "turtleTFmodel" se crea al momento de guardar el modelo ya entrenado con la funcion "model.save()", esto se puede consultar en https://www.tensorflow.org/tutorials/keras/save_and_load, por ejemplo:
  model.save('tfModel/turtleTFmodel', save_format='HDF5')
2. La integración con ROS se basó en https://jacqueskaiser.com/posts/2020/03/ros-tensorflow
