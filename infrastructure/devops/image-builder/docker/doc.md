https://github.com/docker/buildx

https://github.com/docker/build-push-action

https://github.com/google/cadvisor

https://github.com/docker/compose

https://github.com/kubernetes/kompose

https://medium.com/@faruk13/alpine-slim-bullseye-bookworm-noble-differences-in-docker-images-explained-d9aa6efa23ec

https://github.com/wagoodman/dive

https://github.com/GoogleContainerTools/distroless

https://github.com/slimtoolkit/slim

https://docs.docker.com/build/building/best-practices/
https://docs.docker.com/reference/build-checks/

descobrir versão das lib instaladas numa imagem docker
docker run --rm <image-name> bash -c "pip list"
docker run -it --rm image bash | e procurar arquivo requirements.txt

limpar a porra toda
docker system prune -a

https://github.com/distribution/distribution/
https://github.com/opencontainers/distribution-spec
https://github.com/opencontainers/image-spec
https://github.com/opencontainers/runtime-spec

https://public.cyber.mil/devsecops_enterprise_container_image_creation_and_deployment_guide_2/
https://dl.dod.cyber.mil/wp-content/uploads/devsecops/pdf/DevSecOps_Enterprise_Container_Image_Creation_and_Deployment_Guide_2.6-Public-Release.pdf

usar essa merda de comando q não tá na porra da documentação depois de instalar o docker
sudo usermod -aG docker $USER
