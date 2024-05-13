from typing import List

from dask_image.imread import imread
from magicgui.widgets import ComboBox, Container
import napari
import numpy as np

COLOR_CYCLE = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf'
]


def create_label_menu(shapes_layer, labels):
    """Create a label menu widget that can be added to the napari viewer dock

    Parameters
    ----------
    shapes_layer : napari.layers.Shapes
        a napari shapes layer
    labels : List[str]
        list of the labels for each keyshape to be annotated (e.g., the body parts to be labeled).

    Returns
    -------
    label_menu : Container
        the magicgui Container with our dropdown menu widget
    """
    # Create the label selection menu
    label_menu = ComboBox(label='feature_label', choices=labels)
    label_widget = Container(widgets=[label_menu])


    def update_label_menu(event):
        """Update the label menu when the shape selection changes"""
        new_label = str(shapes_layer.current_properties['label'][0])
        if new_label != label_menu.value:
            label_menu.value = new_label

    shapes_layer.events.current_properties.connect(update_label_menu)

    def label_changed(new_label):
        """Update the Shapes layer when the label menu selection changes"""
        current_properties = shapes_layer.current_properties
        current_properties['label'] = np.asarray([new_label])
        shapes_layer.current_properties = current_properties
        shapes_layer.refresh_colors()

    label_menu.changed.connect(label_changed)

    return label_widget


def shape_annotator(
        im_path: str,
        labels: List[str],
):
    """Create a GUI for annotating shapes in a series of images.

    Parameters
    ----------
    im_path : str
        glob-like string for the images to be labeled.
    labels : List[str]
        list of the labels for each keyshape to be annotated (e.g., the body parts to be labeled).
    """
    stack = imread(im_path)

    viewer = napari.view_image(stack)
    shapes_layer = viewer.add_shapes(
        ndim=3,
        property_choices={'label': labels},
        edge_color='label',
        edge_color_cycle=COLOR_CYCLE,
        # symbol='o',
        face_color='transparent',
        edge_width=0.5,  # fraction of shape size
        # size=12,
    )
    shapes_layer.edge_color_mode = 'cycle'

    # add the label menu widget to the viewer
    label_widget = create_label_menu(shapes_layer, labels)
    viewer.window.add_dock_widget(label_widget)

    @viewer.bind_key('.')
    def next_label(event=None):
        """Keybinding to advance to the next label with wraparound"""
        current_properties = shapes_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        new_ind = (ind + 1) % len(labels)
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        shapes_layer.current_properties = current_properties
        shapes_layer.refresh_colors()

    def next_on_click(layer, event):
        """Mouse click binding to advance the label when a shape is added"""
        if layer.mode == 'add':
            # By default, napari selects the shape that was just added.
            # Disable that behavior, as the highlight gets in the way
            # and also causes next_label to change the color of the
            # shape that was just added.
            layer.selected_data = set()
            next_label()

    shapes_layer.mode = ''
    shapes_layer.mouse_drag_callbacks.append(next_on_click)

    @viewer.bind_key(',')
    def prev_label(event):
        """Keybinding to decrement to the previous label with wraparound"""
        current_properties = shapes_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        n_labels = len(labels)
        new_ind = ((ind - 1) + n_labels) % n_labels
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        shapes_layer.current_properties = current_properties
        shapes_layer.refresh_colors()

    napari.run()

if __name__ == '__main__':
    shape_annotator('/Users/nicholb/Documents/segmentation/Germband_Extension/Td_Germband_Hoechst_pMad555_20240214_Embryo01.tif', ['head', 'tail', 'left fin', 'right fin'])