![Solid](https://avatars.githubusercontent.com/u/100875314?s=200&v=4)
# Hands on PySpark
# Inicializando o docker e subindo o container com jupyter e spark

```sh
sudo service docker start

docker run --name spark -p 8888:8888 -v /home/andreolv/Desktop/pyspark:/home/jovyan/pyspark jupyter/all-spark-notebook:spark-3.3.0

```

Substitua o path '/home/andreolv/Desktop/pyspark' do meu exemplo pelo path onde se encontram seus jupyter notebooks

# Clique no link gerado no seu terminal e bora pro jupyter!

<p align="center">
  <img src="pyspark.jpg" title="hover text">
</p>
