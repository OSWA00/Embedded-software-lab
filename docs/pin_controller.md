# Pin controller CRUD operations

## POST pins/ : 
Create a new pin

where the posted data is JSON looking something like the following:
```
{
    "pin_num": 23,
    "color": "red",
    "state": "on"
}
```

STATUS Code 201 Created - the new resource is returned in the body of the message

## GET pins/: 
Fetch (Read) all pins stored on the system - STATUS 200 on success

e.g:
```
  {
      "id": "1",
      "pin_num": 23,
      "color": "red",
      "state": "on"
  },
  {
      "id": "2",
      "pin_num": 24,
      "color": "blue",
      "state": "off"
  }
```

## GET pins/id: 
Fetch a pin given its resource identifier - STATUS 200 on success
```
    {
        "id": "2",
        "pin_num": 24,
        "color": "blue",
        "state": "off"
    }
```
## PUT pins/<id> : 
Update a pin given its resource id - STATUS 200 on success

Generally in RESTful APIs a PUT should send an entire resource for updating.

Update all fields (except for its uid which is READONLY)

e.g. Update all fields of pin with id 2:
```
PUT /pins/2
{
    "pin_num": 24,
    "color": "blue",
    "state": "off"
}
```

## DELETE pins/id : 
Delete pin from system - STATUS 204 : Ok, no content

## PATCH pins/id : 
Partially Update a pin given its resource id - STATUS 200 on success

You can update a single field, or all fields (except for its uid which is READONLY)
e.g. Update the state of pin with id 2:
```
PUT /pins/2
{"state": "off"}`
```