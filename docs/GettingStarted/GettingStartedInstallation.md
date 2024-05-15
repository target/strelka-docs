## Installation
Strelka can be installed on any system that can run [containers](https://www.docker.com/resources/what-container). For convenience, the project ships with [docker-compse](https://docs.docker.com/compose/) configuration files for standing up a "quickstart" cluster (found under the `build/` directory). We do not recommend using and do not plan to support OS-native installations.

### Client Install
Strelka's core client apps are written in Go and can be run natively on a host or inside of a container. The following are multiple ways to install each of the apps.

#### strelka-fileshot (build)
1. Build the binary directly from github
    ```sh
    go build github.com/target/strelka/src/go/cmd/strelka-fileshot
    ```

#### strelka-fileshot (build)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the application
    ```sh
    cd /opt/strelka/src/go/cmd/strelka-fileshot/
    go build -o strelka-fileshot .
    ```

#### strelka-fileshot (container)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the container
    ```sh
    cd /opt/strelka/
    docker build -f build/go/fileshot/Dockerfile -t strelka-fileshot .
    ```

#### strelka-oneshot (Build the binary directly from github)
1. Build the binary
    ```sh
    go build github.com/target/strelka/src/go/cmd/strelka-oneshot
    ```

#### strelka-oneshot (build)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the application
    ```sh
    cd /opt/strelka/src/go/cmd/strelka-oneshot/
    go build -o strelka-oneshot .
    ```

#### strelka-oneshot (container)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the container
    ```sh
    cd /opt/strelka/
    docker build -f build/go/oneshot/Dockerfile -t strelka-oneshot .
    ```

#### strelka-filestream (Build the binary directly from github)
1. Build the binary
    ```sh
    go build github.com/target/strelka/src/go/cmd/strelka-filestream
    ```

#### strelka-filestream (build)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the application
    ```sh
    cd /opt/strelka/src/go/cmd/strelka-filestream/
    go build -o strelka-filestream .
    ```

#### strelka-filestream (container)
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the container
    ```sh
    cd /opt/strelka/
    docker build -f build/go/filestream/Dockerfile -t strelka-filestream .
    ```

### Server Install
Strelka's core server components are written in Go and Python 3.9+ and are run from containers. The simplest way to run them is to use docker-compose -- see `build/docker-compose.yaml` for a sample configuration.

#### Docker
1. Clone this repository
    ```sh
    git clone https://github.com/target/strelka.git /opt/strelka/
    ```

2. Build the cluster
    ```sh
    cd /opt/strelka/
    docker-compose -f build/docker-compose.yaml up -d