from django import forms

class DeviceForm(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    template_id = forms.CharField(label='template_id', max_length=200)

class CreateVlanForm(forms.Form):
    vlanNumber = forms.CharField(label='vlanNumber', max_length=50)

class AssignVLanToInterfacesForm(forms.Form):
    # vlanNumber = forms.CharField(label='vlanNumber', max_length=50)
    interfaces = forms.MultipleChoiceField(label='interfaces')
    # vlanMask = forms.CharField(label='vlanMask', max_length=50)
    # vlanDefaultGateway = forms.CharField(label='vlanDefaultGateway', max_length=50)

class GuestIpAddressForm(forms.Form):
    guestIpAddress = forms.CharField(label='guestIpAddress', max_length=50)
    guestMask = forms.CharField(label='guestMask', max_length=50)
    guestDefaultGateway = forms.CharField(label='guestDefaultGateway', max_length=50)

class AddStaticRouteForm(forms.Form):
    routeIpAddress = forms.CharField(label='routeIpAddress', max_length=50)
    routeMask = forms.CharField(label='routeMask', max_length=50)
    routeDefaultGateway = forms.CharField(label='routeDefaultGateway', max_length=50)
