from enum import Enum
from typing import List, TypedDict, NewType, Optional, Union



def _form_params(params):
    """
    Drop None values, send booleans as "true"/"false" and use the Backlog names of the list parameters.
    """
    request_param = {}
    for k, v in params.items():
        if v is None:
            continue
        if type(v) is bool:
            v = "true" if v else "false"
        if k in ("applicableIssueTypes", "items"):
            k += "[]"
        request_param[k] = v
    return request_param

class CustomFieldResponse(TypedDict):
    id: int
    projectId: int
    typeId: int
    version: str
    name: str
    description: str
    required: bool
    useIssueType: bool
    applicableIssueTypes: List[int]
    displayOrder: int


class _InitialDate(TypedDict):
    id: int
    shift: Optional[int]
    date: Optional[str]


class NumberCustomFieldResponse(CustomFieldResponse):
    min: int
    max: int
    initialValue: int
    unit: str
    initialDate: _InitialDate


class DateCustomFieldResponse(CustomFieldResponse):
    min: str
    max: str
    initialValueType: int
    initialDate: str
    initialShift: int


class _ListCustomFieldResponseItem(TypedDict):
    id: int
    name: str
    displayOrder: int


class ListCustomFieldResponse(CustomFieldResponse):
    items: List[_ListCustomFieldResponseItem]
    allowInput: bool
    allowAddItem: bool


AddTextCustomFieldResponse = NewType("AddTextCustomFieldResponse", CustomFieldResponse)
AddSentenceCustomFieldResponse = NewType("AddSentenceCustomFieldResponse", CustomFieldResponse)
AddNumberCustomFieldResponse = NewType("AddNumberCustomFieldResponse", NumberCustomFieldResponse)
AddDateCustomFieldResponse = NewType("AddDateCustomFieldResponse", DateCustomFieldResponse)
AddSingleListCustomFieldResponse = NewType("AddSingleListCustomFieldResponse", ListCustomFieldResponse)
AddMultipleListCustomFieldResponse = NewType("AddMultipleListCustomFieldResponse", ListCustomFieldResponse)
AddCheckboxCustomFieldResponse = NewType("AddCheckboxCustomFieldResponse", ListCustomFieldResponse)
AddRadioCustomFieldResponse = NewType("AddRadioCustomFieldResponse", ListCustomFieldResponse)
AddCustomFiledResponse = Union[
    AddTextCustomFieldResponse, AddSentenceCustomFieldResponse,
    AddNumberCustomFieldResponse, AddDateCustomFieldResponse,
    AddSingleListCustomFieldResponse, AddMultipleListCustomFieldResponse,
    AddCheckboxCustomFieldResponse, AddRadioCustomFieldResponse,
]

DeleteTextCustomFieldResponse = NewType("DeleteTextCustomFieldResponse", CustomFieldResponse)
DeleteSentenceCustomFieldResponse = NewType("DeleteSentenceCustomFieldResponse", CustomFieldResponse)
DeleteNumberCustomFieldResponse = NewType("DeleteNumberCustomFieldResponse", NumberCustomFieldResponse)
DeleteDateCustomFieldResponse = NewType("DeleteDateCustomFieldResponse", DateCustomFieldResponse)
DeleteSingleListCustomFieldResponse = NewType("DeleteSingleListCustomFieldResponse", ListCustomFieldResponse)
DeleteMultipleListCustomFieldResponse = NewType("DeleteMultipleListCustomFieldResponse", ListCustomFieldResponse)
DeleteCheckboxCustomFieldResponse = NewType("DeleteCheckboxCustomFieldResponse", ListCustomFieldResponse)
DeleteRadioCustomFieldResponse = NewType("DeleteRadioCustomFieldResponse", ListCustomFieldResponse)
DeleteCustomFiledResponse = Union[
    DeleteTextCustomFieldResponse, DeleteSentenceCustomFieldResponse,
    DeleteNumberCustomFieldResponse, DeleteDateCustomFieldResponse,
    DeleteSingleListCustomFieldResponse, DeleteMultipleListCustomFieldResponse,
    DeleteCheckboxCustomFieldResponse, DeleteRadioCustomFieldResponse,
]


class CustomField(object):
    class TypeId(Enum):
        TEXT = 1
        SENTENCE = 2
        NUMBER = 3
        DATE = 4
        SINGLE_LIST = 5
        MULTIPLE_LIST = 6
        CHECKBOX = 7
        RADIO = 8

    class DateInitialValueType(Enum):
        TODAY = 1
        TODAY_PLUS_INITIAL_SHIFT = 2
        SPECIFIED_DAY = 3

    def __init__(self, api) -> None:
        self.api = api

    def list(self, projectIdOrKey: str):
        """List custom fields
        https://developer.nulab.com/docs/backlog/api/2/get-custom-field-list/

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        """
        _url = f"projects/{projectIdOrKey}/customFields"
        _method = "GET"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()

    def add(
        self,
        projectIdOrKey: str,
        typeId: Union[TypeId, int],
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        **kwargs,
    ) -> AddCustomFiledResponse:
        """Add custom field
        https://developer.nulab.com/docs/backlog/api/2/add-custom-field/#
        """
        _url = f"projects/{projectIdOrKey}/customFields"
        _method = "POST"
        tid = typeId
        if isinstance(typeId, Enum):
            tid = typeId.value
        elif isinstance(typeId, int):
            tid = typeId
        else:
            raise ValueError(f"invalid typeId: {typeId}")
        request_param = _form_params({
            "typeId": tid,
            "name": name,
            "applicableIssueTypes": applicableIssueTypes,
            "description": description,
            "required": required,
            **kwargs,
        })

        resp = self.api.invoke_method(_method, _url, request_param=request_param)

        return resp.json()

    def add_text_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> AddTextCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            1,
            name,
            applicableIssueTypes,
            description,
            required,
        )

    def add_sentence_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> AddSentenceCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            2,
            name,
            applicableIssueTypes,
            description,
            required,
        )

    def add_number_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        min: Optional[int] = None,
        max: Optional[int] = None,
        initialValue: Optional[int] = None,
        unit: Optional[str] = None,
    ) -> AddNumberCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            3,
            name,
            applicableIssueTypes,
            description,
            required,
            min=min,
            max=max,
            initialValue=initialValue,
            unit=unit,
        )

    def add_date_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        min: Optional[str] = None,  # yyyy-MM-dd
        max: Optional[str] = None,  # yyyy-MM-dd
        initialValueType: Optional[DateInitialValueType] = None,
        initialDate: Optional[str] = None,  # yyyy-MM-dd
        initialShift: Optional[int] = None,
    ) -> AddDateCustomFieldResponse:
        if isinstance(initialValueType, Enum):
            initialValueType = initialValueType.value

        if (
            (initialValueType == self.DateInitialValueType.SPECIFIED_DAY.value)
            and (initialDate is None)
        ):
            raise ValueError("initialDate is required when initialValueType is SPECIFIED_DAY")

        return self.add(
            projectIdOrKey,
            4,
            name,
            applicableIssueTypes,
            description,
            required,
            min=min,
            max=max,
            initialValueType=initialValueType,
            initialDate=initialDate,
            initialShift=initialShift,
        )

    def add_single_list_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddSingleListCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            5,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_multiple_list_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddMultipleListCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            6,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_checkbox_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddCheckboxCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            7,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_radio_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddRadioCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            8,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def update(
        self,
        projectIdOrKey: str,
        id: int,
        name: Optional[str] = None,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        **kwargs,
    ):
        """Update custom field
        https://developer.nulab.com/docs/backlog/api/2/update-custom-field/

        Requires administrator or project administrator rights.

        :param projectIdOrKey: project id or key
        :param id: custom field id
        :param name: Optional. name
        :param applicableIssueTypes: Optional. issue type IDs the field applies to (empty: all issue types)
        :param description: Optional. description
        :param required: Optional. True to make the field required
        :param kwargs: parameters of the field type, as for add(): min, max, initialValue and unit (number);
            min, max, initialValueType, initialDate and initialShift (date); items, allowInput and allowAddItem (list)
        :return: the updated custom field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}"
        request_param = _form_params({
            "name": name,
            "applicableIssueTypes": applicableIssueTypes,
            "description": description,
            "required": required,
            **kwargs,
        })

        resp = self.api.invoke_method("PATCH", _url, request_param=request_param)

        return resp.json()

    def add_list_item(self, projectIdOrKey: str, id: int, name: str):
        """Add a list item to a list type custom field
        https://developer.nulab.com/docs/backlog/api/2/add-list-item-for-list-type-custom-field/

        :param projectIdOrKey: project id or key
        :param id: custom field id
        :param name: name of the list item
        :return: the custom field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}/items"

        resp = self.api.invoke_method("POST", _url, request_param={"name": name})

        return resp.json()

    def update_list_item(self, projectIdOrKey: str, id: int, itemId: int, name: str):
        """Update a list item of a list type custom field
        https://developer.nulab.com/docs/backlog/api/2/update-list-item-for-list-type-custom-field/

        :param projectIdOrKey: project id or key
        :param id: custom field id
        :param itemId: list item id
        :param name: new name of the list item
        :return: the custom field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}/items/{itemId}"

        resp = self.api.invoke_method("PATCH", _url, request_param={"name": name})

        return resp.json()

    def delete_list_item(self, projectIdOrKey: str, id: int, itemId: int):
        """Delete a list item of a list type custom field
        https://developer.nulab.com/docs/backlog/api/2/delete-list-item-for-list-type-custom-field/

        :param projectIdOrKey: project id or key
        :param id: custom field id
        :param itemId: list item id
        :return: the custom field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}/items/{itemId}"

        resp = self.api.invoke_method("DELETE", _url)

        return resp.json()

    def delete(self, projectIdOrKey: str, id: int) -> DeleteCustomFiledResponse:
        """Delete custom field
        https://developer.nulab.com/docs/backlog/api/2/delete-custom-field/#delete-custom-field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}"
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()
