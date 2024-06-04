# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name

import numpy as np
import pytest
from PIL import Image

from dobble.visual import Visual


class MockVisual(Visual):
    """A mock class for testing purposes."""

    def get_img(
            self,
            outline_only: bool,
            padding: float,
            img_size: int
    ) -> Image.Image:
        return Image.new("RGBA", (img_size, img_size), (255, 255, 255, 255))


@pytest.fixture
def visual():
    return MockVisual()


def test_init(visual):
    assert isinstance(visual, Visual)
    assert visual.rotation == 0


def test_get_array(visual):
    arr = visual.get_array(
        outline_only=False,
        padding=0.05,
        img_size=512
    )
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (512, 512, 4)


def test_reset_rotation(visual):
    visual.rotation = 180
    visual.reset_rotation()
    assert visual.rotation == 0


@pytest.mark.parametrize("degrees", [45, 90, 180, -45, -90, -180])
def test_rotate_with_specified_degrees(visual, degrees):
    previous_rotation = visual.rotation
    new_rotation = visual.rotate(degrees)
    assert (previous_rotation + degrees) % 360 == new_rotation


def test_rotate_with_random_degrees(visual):
    seed = 42
    rng = np.random.default_rng(seed)
    expected_rotation = rng.uniform(0, 360)
    first_rotation = visual.rotate(seed=seed)
    second_rotation = visual.rotate(seed=seed)
    assert expected_rotation == first_rotation == second_rotation


def test_show(mocker, visual):
    mock_show = mocker.patch("PIL.Image.Image.show")
    visual.show(
        outline_only=False,
        padding=0.05,
        img_size=512
    )
    mock_show.assert_called_once()
