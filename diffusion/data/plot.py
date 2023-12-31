import pathlib
from typing import Callable, Optional

import matplotlib.pyplot as plt
import torch

from diffusion.schedule import Scheduler

from .transform import tensor_to_image


def plot_image(
    image: torch.Tensor,
    transform: Callable = tensor_to_image,
    file_path: Optional[pathlib.Path] = None,
) -> None:
    """_summary_

    Parameters
    ----------
    image : torch.Tensor
        _description_
    transform : Callable, optional
        _description_, by default reverse_transform_image
    file_path : Optional[pathlib.Path], optional
        _description_, by default None
    """
    if file_path is not None:
        plt.imsave(file_path, transform(image))
    else:
        plt.imshow(transform(image))


def plot_schedule(
    scheduler: Scheduler,
    time_steps: int = 1000,
    file_path: Optional[pathlib.Path] = None,
):
    """_summary_

    Parameters
    ----------
    scheduler : Scheduler
        _description_
    time_steps : int, optional
        _description_, by default 1000
    file_path : Optional[pathlib.Path], optional
        _description_, by default None
    """
    title = f"{scheduler.name.capitalize()} Scheduler\n s={scheduler.start}, e={scheduler.end}"
    if scheduler.name != "linear":
        title += f", $\\tau$={scheduler.tau}"
    plt.title(title)
    plt.xlabel("$t$")
    plt.ylabel("$\\gamma(t)$")
    plt.gca().set_aspect("equal", adjustable="box")
    t = torch.linspace(0, 1, time_steps)
    plt.plot(t, scheduler(t))
    if file_path is not None:
        plt.savefig(file_path, bbox_inches="tight", pad_inches=0)
    else:
        plt.show()


def plot_loss(
    losses: torch.Tensor,
    title: str = "Training Loss Over Epochs",
    xlabel: str = "Epoch",
    ylabel: str = "MSE Loss",
    file_path: Optional[pathlib.Path] = None,
) -> None:
    """_summary_

    Parameters
    ----------
    losses : torch.Tensor
        _description_
    title : str, optional
        _description_, by default "Training Loss Over Epochs"
    xlabel : str, optional
        _description_, by default "Epoch"
    ylabel : str, optional
        _description_, by default "MSE Loss"
    file_path : Optional[pathlib.Path], optional
        _description_, by default None
    """
    plt.ylim(0, 1)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(losses)
    if file_path is not None:
        plt.savefig(file_path)
    else:
        plt.show()


def plot_denoising_results(
    t: torch.Tensor,
    image_noised: torch.Tensor,
    image_restored: torch.Tensor,
    noise: torch.Tensor,
    noise_predicted: torch.Tensor,
    transform: Callable = tensor_to_image,
    file_path: Optional[pathlib.Path] = None,
) -> None:
    """_summary_

    Parameters
    ----------
    t : torch.Tensor
        _description_
    imag_noised : torch.Tensor
        _description_
    image_restored : torch.Tensor
        _description_
    noise : torch.Tensor
        _description_
    noise_predicted : torch.Tensor
        _description_
    transform : Callable, optional
        _description_, by default reverse_transform_image
    file_path : Optional[pathlib.Path], optional
        _description_, by default None
    """
    # Prepare the figure
    plt.figure(figsize=(30, 30))
    fig, axes = plt.subplots(2, 2, figsize=(5, 5))
    fig.suptitle(f"Image Denoising at t=${t[0]}$", fontsize=14)
    fig.tight_layout()
    for ax in axes.ravel():
        ax.axis("off")
    # First subplot
    ax0 = axes[0, 0]
    ax0.imshow(transform(image_noised.squeeze()))
    ax0.set_title(f"Noisy Image at Time ${t[0]}$", fontsize=10)
    # Second subplot
    ax1 = axes[0, 1]
    ax1.imshow(transform(image_restored.squeeze()))
    ax1.set_title(f"Restored Image", fontsize=10)
    # Third subplot
    ax2 = axes[1, 0]
    ax2.imshow(transform(noise.squeeze()))
    ax2.set_title(f"Ground Truth Noise", fontsize=10)
    # Fourth subplot
    ax3 = axes[1, 1]
    ax3.imshow(transform(noise_predicted.squeeze()))
    ax3.set_title(f"Predicted Noise", fontsize=10)
    if file_path is not None:
        plt.savefig(file_path)
    else:
        plt.show()
