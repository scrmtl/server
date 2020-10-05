from .. import serializers
from .. import models
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, \
    TokenHasScope
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions


def deep_copy_model(self, model, updated_fk=None, related_field=None):
    child_model_relationships = []
    # Take the passed in model and get the relationships of that model
    relations = [
        f for f in model._meta.get_fields()
        if (f.one_to_many or f.one_to_one)
        and f.auto_created and not f.concrete
    ]
    # Get the list of related models for those relationships
    for relation in relations:
        accessor_name = relation.get_accessor_name()
        # Get the related field name for each relationship
        fk_field = relation.field.get_attname()
        # Build a list of child model list and related field name pairs
        child_model_relationships.append(
            (getattr(model, accessor_name).all(), fk_field))

    # Make a copy of the model
    model.pk = None

    # If a parent model pk and related field are passed in, change that
    # related field to the parent pk
    # if updated_fk:
    # This is what I am unable to fix.  Need to dynamically reference the
    # models fk field to update with parent pk
    # getattr(model, related_field) = updated_fk
    # model.label_id = updated_fk
    # getattr(model, related_field) = updated_fk
    # getattr(model, related_field).SET(updated_fk)

    model.save()

    # Record the copied model's pk
    new_pk = model.pk
    # Loop through the listed pairs, deep copying each model and passing
    # the pk and field name to update
    for child_model_relationship in child_model_relationships:
        for child_model in child_model_relationship[0]:
            self.deep_copy_model(
                model=child_model,
                updated_fk=new_pk,
                related_field=child_model_relationship[1])

    return model.pk
