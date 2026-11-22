# PIXM XSD patterns

Templates for the type families named in CLAUDE.md §3.2–§3.4. Each pattern shows
the **current** form found in the schema and the **target** form that new or
touched elements must follow. The difference is mostly documentation and, for
measures, the required `uom`.

## 1. Codelist: `Code…BaseType` + `Code…Type`

The base type is an `xs:union` (even with one member) so the grandfathered
`OTHER` pattern can sit alongside the enumeration. New codelists have no `OTHER`
member unless the CCB approves one.

```xml
<!-- PIXM_Codelists.xsd -->
<xs:simpleType name="CodeOnOffBaseType">
  <xs:annotation>
    <xs:documentation>The state of a system that can be switched on or off. [PIXM]</xs:documentation>
  </xs:annotation>
  <xs:union>
    <xs:simpleType>
      <xs:restriction base="xs:string">
        <xs:enumeration value="OFF">
          <xs:annotation><xs:documentation>The system is switched off.</xs:documentation></xs:annotation>
        </xs:enumeration>
        <xs:enumeration value="ON">
          <xs:annotation><xs:documentation>The system is switched on.</xs:documentation></xs:annotation>
        </xs:enumeration>
      </xs:restriction>
    </xs:simpleType>
  </xs:union>
</xs:simpleType>

<!-- PIXM_DataTypes.xsd -->
<xs:complexType name="CodeOnOffType">
  <xs:annotation>
    <xs:documentation>The state of a system that can be switched on or off, with an optional reason when the value is not provided. [PIXM]</xs:documentation>
  </xs:annotation>
  <xs:simpleContent>
    <xs:extension base="pixm:CodeOnOffBaseType">
      <xs:attribute name="nilReason" type="gml:NilReasonEnumeration"/>
    </xs:extension>
  </xs:simpleContent>
</xs:complexType>
```

Grandfathered `OTHER` member (existing codelists only):

```xml
<xs:simpleType>
  <xs:restriction base="xs:string">
    <xs:pattern value="OTHER(:(\w|_){1,58})?"/>
  </xs:restriction>
</xs:simpleType>
```

## 2. Measure with a unit: `Val…BaseType` + `Val…Type` + `Uom…Type`

`uom` is **required** (units rule, CLAUDE.md §3.2). Existing measures still have it
optional; that is a known defect.

```xml
<!-- PIXM_UoM.xsd -->
<xs:simpleType name="UomDistanceType">
  <xs:annotation><xs:documentation>Units of measurement for horizontal distance. [PIXM]</xs:documentation></xs:annotation>
  <xs:restriction base="xs:string">
    <xs:enumeration value="FT"><xs:annotation><xs:documentation>Foot.</xs:documentation></xs:annotation></xs:enumeration>
    <xs:enumeration value="M"><xs:annotation><xs:documentation>Meter.</xs:documentation></xs:annotation></xs:enumeration>
    <!-- … -->
  </xs:restriction>
</xs:simpleType>

<!-- PIXM_Measures.xsd -->
<xs:simpleType name="ValDistanceBaseType">
  <xs:annotation><xs:documentation>A non-negative horizontal distance value. [PIXM]</xs:documentation></xs:annotation>
  <xs:restriction base="xs:decimal">
    <xs:minInclusive value="0"/>
  </xs:restriction>
</xs:simpleType>

<xs:complexType name="ValDistanceType">
  <xs:annotation><xs:documentation>A horizontal distance with its unit of measurement. [PIXM]</xs:documentation></xs:annotation>
  <xs:simpleContent>
    <xs:extension base="pixm:ValDistanceBaseType">
      <xs:attribute name="uom" type="pixm:UomDistanceType" use="required"/>
      <xs:attribute name="nilReason" type="gml:NilReasonEnumeration"/>
    </xs:extension>
  </xs:simpleContent>
</xs:complexType>
```

## 3. Dimensionless measure

No `uom`. The definition must say "dimensionless" and state the range or scale.

```xml
<xs:simpleType name="ValMuBaseType">
  <xs:annotation><xs:documentation>A runway friction coefficient. Dimensionless; range greater than 0 and less than 1. [PIXM]</xs:documentation></xs:annotation>
  <xs:restriction base="xs:decimal">
    <xs:minExclusive value="0.0"/>
    <xs:maxExclusive value="1.0"/>
  </xs:restriction>
</xs:simpleType>
```

## 4. Constrained text: `Text…BaseType` + `Text…Type`

```xml
<xs:simpleType name="TextSettingBaseType">
  <xs:annotation><xs:documentation>… [PIXM]</xs:documentation></xs:annotation>
  <xs:restriction base="pixm:Character2Type">
    <xs:maxLength value="80"/>
  </xs:restriction>
</xs:simpleType>

<xs:complexType name="TextSettingType">
  <xs:annotation><xs:documentation>… [PIXM]</xs:documentation></xs:annotation>
  <xs:simpleContent>
    <xs:extension base="pixm:TextSettingBaseType">
      <xs:attribute name="nilReason" type="gml:NilReasonEnumeration"/>
    </xs:extension>
  </xs:simpleContent>
</xs:complexType>
```

Use free text only where the CCB has approved it (CLAUDE.md §2).

## 5. Feature and time slice

AIXM 5.1.1 pattern (DEC-0003): the feature's `timeSlice` property holds a
`…TimeSlicePropertyType`, which contains the named `…TimeSlice` element.

```xml
<xs:element name="TakeoffRequestTimeSlice" type="pixm:TakeoffRequestTimeSliceType"
            substitutionGroup="pixm:AbstractPIXMTimeSlice"/>
<xs:element name="TakeoffRequest" type="pixm:TakeoffRequestType"
            substitutionGroup="pixm:AbstractPIXMFeature"/>

<xs:complexType name="TakeoffRequestTimeSliceType">
  <xs:annotation><xs:documentation>… [PIXM]</xs:documentation></xs:annotation>
  <xs:complexContent>
    <xs:extension base="pixm:AbstractPIXMTimeSliceType">
      <xs:sequence>
        <xs:element name="zeroFuelWeight" type="pixm:ValWeightType" minOccurs="0" maxOccurs="1">
          <xs:annotation><xs:documentation>… [PIXM]</xs:documentation></xs:annotation>
        </xs:element>
        <!-- … -->
      </xs:sequence>
    </xs:extension>
  </xs:complexContent>
</xs:complexType>

<xs:complexType name="TakeoffRequestType">
  <xs:annotation><xs:documentation>… [PIXM]</xs:documentation></xs:annotation>
  <xs:complexContent>
    <xs:extension base="pixm:AbstractPIXMFeatureType">
      <xs:sequence>
        <xs:element name="timeSlice" type="pixm:TakeoffRequestTimeSlicePropertyType" minOccurs="1" maxOccurs="unbounded">
          <xs:annotation><xs:documentation>A time slice of the Takeoff Request feature: its state during one period of validity. [AIXM 5.1.1]</xs:documentation></xs:annotation>
        </xs:element>
      </xs:sequence>
    </xs:extension>
  </xs:complexContent>
</xs:complexType>

<xs:complexType name="TakeoffRequestTimeSlicePropertyType">
  <xs:annotation><xs:documentation>A property that contains one Takeoff Request time slice. [AIXM 5.1.1]</xs:documentation></xs:annotation>
  <xs:sequence>
    <xs:element ref="pixm:TakeoffRequestTimeSlice" minOccurs="1" maxOccurs="1"/>
  </xs:sequence>
  <xs:attributeGroup ref="gml:OwnershipAttributeGroup"/>
</xs:complexType>
```

Instance:

```xml
<pixm:TakeoffRequest gml:id="to-req-28R">
  <pixm:timeSlice>
    <pixm:TakeoffRequestTimeSlice gml:id="to-req-28R-ts">
      <gml:validTime>…</gml:validTime>
      <pixm:interpretation>BASELINE</pixm:interpretation>
      …
    </pixm:TakeoffRequestTimeSlice>
  </pixm:timeSlice>
</pixm:TakeoffRequest>
```

The abstract substitution heads are `pixm:AbstractPIXMFeature` (in
`gml:AbstractFeature`) and `pixm:AbstractPIXMTimeSlice` (in `gml:AbstractTimeSlice`).

## 6. Reference to an external AIXM feature

Target pattern for replacing the AIXM import (known defect). To be designed and
approved on the `known-defects` branch; shape will be an xlink reference to the
AIXM feature identifier plus an optional human-readable designator.
`TODO(CCB)`: confirm final structure.

## 7. Checklist for a new or touched element

- Named, global type; correct family pattern (§1–§5).
- `xs:documentation` on the type, each property and each literal, ending with a source tag.
- `pixm:` prefix on every PIXM type reference.
- `minOccurs` and `maxOccurs` explicit; `minOccurs="0"` unless the parent is meaningless without it.
- No XSD primitives directly on properties.
- Measures follow the units rule.
