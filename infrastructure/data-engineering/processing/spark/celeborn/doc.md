https://github.com/apache/celeborn

helm chart não funciona
https://github.com/apache/celeborn/issues/2744
projeto não tem imagem docker oficial WTF? já mostra o nível de maturidade do projeto
precisa clonar repo e buildar imagem

Maybe you want to make your own celeborn docker image, you can use docker build . -f docker/Dockerfile in Celeborn Binary.
https://github.com/apache/celeborn/blob/main/docker/Dockerfile

mas to com preguiça de fazer isso
