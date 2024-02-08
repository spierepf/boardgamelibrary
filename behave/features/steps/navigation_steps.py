from behave import *


@when(u'we open the create new copy form')
def step_impl(context):
    context.execute_steps('When we click on the component with id "open_user_menu"')
    context.execute_steps('When we click on the component with id "open_create_new_copy_form"')
    context.execute_steps('Then we will see a component with id "create_new_copy_form"')


@when(u'we create a copy of the {year} edition of "{title}" for the logged in user')
@when(u'we create a copy of the {year} edition of "{title}" for "{username}"')
def step_impl(context, year, title, username=None):
    context.execute_steps('When we open the create new copy form')
    if username is not None:
        context.execute_steps(f'When we select the "{username}" option in the select component with id "copy_owner"')
    context.execute_steps(f'When we enter the value "{title}" into the component with id "copy_title"')
    context.execute_steps(f'When we click on the "{title} ({year})" option in the autocomplete component with id "copy_title"')
    context.execute_steps('When we click on the component with id "submit"')
