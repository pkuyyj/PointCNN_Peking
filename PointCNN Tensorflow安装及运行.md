## PointCNN Tensorflow安装及运行

### 安装环境

系统：CentOS7 Linux

Conda版本：miniconda3

### 具体安装顺序

#### 1. 新建python3.6环境

按照Tensorflow的版本要求，需要python版本3.5-3.6，CUDA 9.0，cuDNN 7.0

 ```bash
 conda create -n tf python=3.6
 conda activate tf
 ```

#### 2.1 CPU版本：安装Cuda Toolkit、cuDNN、tensorflow、h5py

```bash
conda install cudnn=7.0 h5py tensorflow=1.6
```

以下用`tf_cpu`代指此环境

#### 2.2 GPU版本：

##### 2.2.1 配置CUDA环境

为了使用GPU版本的tf 1.6，需要CUDA 9.0；一般电脑和服务器都是CUDA 10以上，所以需要重装，集群上在`/opt/cuda-9.0`下，故需要在`.bashrc`中导入环境变量

```bash
export PATH=/opt/cuda-9.0/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/opt/cuda-9.0/lib64/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

##### 2.2.2 安装依赖库

```bash
conda install cudnn=7.0 h5py tensorflow_gpu=1.6
```

以下用`tf_gpu`代指此环境

### 运行

#### 1.原始PointCNN.Pytorch

数据集：原始数据集

在`PointCNN.Pytorch\sem_seg`下执行

##### CPU版本：

```bash
conda activate tf_cpu
python train.py --batch_size 12 --max_epoch 50
```

##### GPU版本：

```bash
conda activate tf_gpu
CUDA_VISIBLE_DEVICES=1,2 python train.py --batch_size 24 --max_epoch 50 --gpu 0
```

注：由于GPU较快，可以适当增加batch size; CUDA_VISIBLE_DEVICES按照当时空闲GPU序号填写

此处的train.py为原始文件，需要修改`dataset`的路径并提前准备好ModelNet40和indoor_h5数据集.

运行日志保存在`log`文件夹下，具体训练日志可以通过以下方式查看

```bash
cd log
vi log_train.txt
```

#### 2.应用在SemanticPOSS上的PointCNN.Pytorch

##### CPU版本：

在`PointCNN_semantic_segmantation`下执行

```bash
conda activate tf_cpu
python train.py --batch_size 12 
```

##### GPU版本：

由于POSS数据集较大，无法全部放入内存，故需要进行降采样。具体步骤如下：

```bash
cd ~/PointCNN_downs
conda activate tf_gpu
CUDA_VISIBLE_DEVICES=1,2 python train.py --batch_size 12 --max_epoch 100 --gpu 0 --learning_rate 0.001
```

实际上，只会用到一个GPU.
