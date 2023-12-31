import os
import pathlib
from typing import Callable, List, Literal, Optional, Tuple

import torch
from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import transforms
from torchvision.datasets import (
    CIFAR10,
    LSUN,
    MNIST,
    CelebA,
    FGVCAircraft,
    VisionDataset,
)

from .transform import image_to_tensor


def load_images(
    file_path: pathlib.Path,
    transformation: Callable = image_to_tensor,
    device: torch.device = torch.device("cpu"),
) -> torch.Tensor:
    """_summary_

    Parameters
    ----------
    file_path : pathlib.Path
        The path to the image. If it is a directory, all images in the directory are loaded.
    transformation : Callable, optional
        The transformation that is applied to the images, by default image_to_tensor()
    device : torch.device, optional
        The device, by default torch.device("cpu")

    Returns
    -------
    torch.Tensor
        The tensor containing the images.
    """
    if file_path.is_dir():
        tensors: List[torch.Tensor] = []
        for file in file_path.iterdir():
            image = Image.open(file).convert("RGB")
            tensor = transformation(image).to(device)
            tensors.append(tensor)
        return torch.stack(tensors)
    else:
        image = Image.open(file_path)
        return transformation(image).to(device)


def load_dataset(
    name: Literal["cifar10", "mnist", "aircraft", "lsun", "celeba"],
    transform: Callable = image_to_tensor,
    download: bool = True,
    outdir: pathlib.Path = pathlib.Path("../data/datasets/"),
    device: torch.device = torch.device("cpu"),
) -> VisionDataset:
    """_summary_

    Parameters
    ----------
    name : Literal["cifar10", "minst", "aircraft", "lsun", "celeba"]
        _description_
    transform : Callable, optional
        _description_, by default image_to_tensor()
    download : bool, optional
        _description_, by default True
    outdir : pathlib.Path, optional
        _description_, by default "../data/datasets/"
    device : torch.device, optional
        _description_, by default torch.device("cpu")

    Returns
    -------
    VisionDataset
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    # Ensure that the data folder exists
    outdir = outdir / name
    if not outdir.exists():
        os.makedirs(outdir)
    # Download the dataset
    if name == "cifar10":
        return CIFAR10(
            root=outdir, download=download, transform=transform, device=device
        )
    elif name == "mnist":
        return MNIST(root=outdir, download=download, transform=transform, device=device)
    elif name == "aircraft":
        return FGVCAircraft(
            root=outdir, download=download, transform=transform, device=device
        )
    elif name == "celeba":
        return CelebA(
            root=outdir, download=download, transform=transform, device=device
        )
    elif name == "lsun":
        return LSUN(
            root=outdir,
            classes=["bedroom"],
            download=download,
            transform=transform,
            device=device,
        )
    else:
        raise ValueError(f'Invalid dataset specified: "{name}".')


def split_dataset(
    dataset: Dataset,
    train_size,
    random_state: int = 0,
) -> Tuple[List[int], List[int]]:
    """_summary_

    Parameters
    ----------
    dataset : Dataset
        _description_
    train_size : float, optional
        _description_, by default 0.8
    random_state : int, optional
        _description_, by default 0

    Returns
    -------
    Tuple[List[int], List[int]]
        _description_
    """
    # Generate the train and test indices
    train_indices, test_indices, _, _ = train_test_split(
        range(len(dataset)),
        dataset.targets,
        stratify=dataset.targets,
        train_size=train_size,
        shuffle=True,
        random_state=random_state,
    )
    return train_indices, test_indices


def create_dataloader(
    dataset: Dataset, indices: Optional[torch.Tensor] = None, batch_size: int = 16
) -> DataLoader:
    """_summary_

    Parameters
    ----------
    dataset : Dataset
        _description_
    indices : Optional[torch.Tensor], optional
        _description_, by default None
    batch_size : int, optional
        _description_, by default 16

    Returns
    -------
    DataLoader
        _description_
    """
    if indices is not None:
        dataset = Subset(dataset, indices)
    return DataLoader(dataset, batch_size=batch_size)
