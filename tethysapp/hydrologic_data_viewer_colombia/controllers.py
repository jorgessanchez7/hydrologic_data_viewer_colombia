from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'hydrologic_data_viewer_colombia/home.html', context)

def hobs(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/hobs.html')

def hsen(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/hsen.html')

def qobs(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/qobs.html')

def qsen(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/qsen.html')

def about(request):
    """
    Controller for the app about page.
    """

    return render(request, 'hydrologic_data_viewer_colombia/about.html')
