# =============================================================================
#               ____ _   _ ____  _          _
#  _ __  _   _ / ___| | | |  _ \| |      __| | ___  _ __ ___
# | '_ \| | | | |  _| |_| | | | | |     / _` |/ _ \| '_ ` _ \
# | |_) | |_| | |_| |  _  | |_| | |___ | (_| | (_) | | | | | |
# | .__/ \__, |\____|_| |_|____/|_____(_)__,_|\___/|_| |_| |_|
# |_|    |___/
# =============================================================================
# Authors:
#   Patrick Lehmann
#
# Package module:   DOM: Attributes.
#
# License:
# ============================================================================
#  Copyright (C) 2019-2022 Tristan Gingold
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <gnu.org/licenses>.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ============================================================================
from typing import List

from pyTooling.Decorators import export
from pyTooling.Warning import WarningCollector

from pyVHDLModel.Name import Name
from pyVHDLModel.Symbol import Symbol
from pyVHDLModel.Declaration import EntityClass, Attribute as VHDLModel_Attribute
from pyVHDLModel.Declaration import AttributeSpecification as VHDLModel_AttributeSpecification

from pyGHDL.libghdl import utils
from pyGHDL.libghdl._types import Iir
from pyGHDL.libghdl.vhdl import nodes
from pyGHDL.libghdl.vhdl.tokens import Tok
from pyGHDL.dom import DOMMixin, Position, DOMException, Expression
from pyGHDL.dom._Utils import GetNameOfNode, GetIirKindOfNode, GetDocumentationOfNode
from pyGHDL.dom._Translate import GetName, GetExpressionFromNode
from pyGHDL.dom.Name import SimpleName
from pyGHDL.dom.Symbol import SimpleSubtypeSymbol


@export
class Attribute(VHDLModel_Attribute, DOMMixin):
    def __init__(self, node: Iir, identifier: str, subtype: Symbol, documentation: str = None) -> None:
        super().__init__(identifier, subtype, documentation)
        DOMMixin.__init__(self, node)

    @classmethod
    def parse(cls, attributeNode: Iir) -> "Attribute":
        name = GetNameOfNode(attributeNode)
        documentation = GetDocumentationOfNode(attributeNode)
        subtypeMark = nodes.Get_Type_Mark(attributeNode)
        subtypeName = GetNameOfNode(subtypeMark)

        subtype = SimpleSubtypeSymbol(subtypeMark, SimpleName(subtypeMark, subtypeName))
        return cls(attributeNode, name, subtype, documentation)


_TOKEN_TRANSLATION = {
    Tok.Entity: EntityClass.Entity,
    Tok.Architecture: EntityClass.Architecture,
    Tok.Configuration: EntityClass.Configuration,
    Tok.Procedure: EntityClass.Procedure,
    Tok.Function: EntityClass.Function,
    Tok.Package: EntityClass.Package,
    Tok.Type: EntityClass.Type,
    Tok.Subtype: EntityClass.Subtype,
    Tok.Constant: EntityClass.Constant,
    Tok.Signal: EntityClass.Signal,
    Tok.Variable: EntityClass.Variable,
    Tok.Component: EntityClass.Component,
    Tok.Label: EntityClass.Label,
    Tok.Literal: EntityClass.Literal,
    Tok.Units: EntityClass.Units,
    Tok.Group: EntityClass.Group,
    Tok.File: EntityClass.File,
    Tok.Property: EntityClass.Property,
    Tok.Sequence: EntityClass.Sequence,
    #    Tok.View: EntityClass.View,
    Tok.Others: EntityClass.Others,
}


@export
class AttributeSpecification(VHDLModel_AttributeSpecification, DOMMixin):
    def __init__(
        self,
        node: Iir,
        identifiers: List[Name],
        attribute: Name,
        entityClass: EntityClass,
        expression: Expression,
        documentation: str = None,
    ) -> None:
        super().__init__(identifiers, attribute, entityClass, expression, documentation)
        DOMMixin.__init__(self, node)

    @classmethod
    def parse(cls, attributeNode: Iir) -> "AttributeSpecification":
        attributeDesignator = nodes.Get_Attribute_Designator(attributeNode)
        attributeName = GetName(attributeDesignator)
        documentation = GetDocumentationOfNode(attributeNode)

        names = []
        entityNameList = nodes.Get_Entity_Name_List(attributeNode)
        for name in utils.flist_iter(entityNameList):
            nameKind = GetIirKindOfNode(name)
            if nameKind == nodes.Iir_Kind.Simple_Name:
                names.append(SimpleName(name, GetNameOfNode(name)))
            elif nameKind == nodes.Iir_Kind.Signature:
                WarningCollector.Raise("[NOT IMPLEMENTED] Signature name in attribute specifications.")
            else:
                position = Position.parse(name)
                raise DOMException(
                    f"Unknown name kind '{nameKind.name}' in attribute specification '{attributeNode}' at {position}."
                )

        entityClassToken = nodes.Get_Entity_Class(attributeNode)
        try:
            entityClass = _TOKEN_TRANSLATION[entityClassToken]
        except KeyError:
            position = Position.parse(attributeNode)
            raise DOMException(
                f"Unknown token '{entityClassToken.name}' in attribute specification for entity class '{attributeNode}' at {position}."
            )

        expression = GetExpressionFromNode(nodes.Get_Expression(attributeNode))

        return cls(attributeNode, names, attributeName, entityClass, expression, documentation)
