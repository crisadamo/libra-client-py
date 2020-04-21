## Getting Started

### Installation

#### Setup
```bash
python -m pip install --upgrade pip
python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
(venv) python -m pip install --upgrade pip
(venv) python -m pip install grpcio
(venv) python -m pip install grpcio-tools
```

#### Generate gRPC stubs
```bash
$ python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/route_guide.proto

find ./ -name '*.proto' -exec cp -prv '{}' '../test-grpc/config/' ';'

python -m grpc_tools.protoc -Iconfig/client/ --python_out=. --grpc_python_out=. config/client/*.proto
```
