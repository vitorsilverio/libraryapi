<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>

    <!--
    XSLT 2.0 stylesheet that takes an XML Pergamum MARC record retrieved by Pergamum web service
    ("busca_marc") and transforms it to a MARCXML record format.
    
    Created on: Jul 12, 2021
    Author: Jaider Andrade Ferreira
    -->

    <!--
    For each "indicador" element, call the template "buildMarcField".
    -->

    <xsl:template match="/">
        <collection xmlns="http://www.loc.gov/MARC21/slim">
            <record>
                <!-- 
                Careful: the leader field must have appropriate 
                blank spaces: _____nam_a22______a_4500
                -->
                <leader>
                    <xsl:text>     nam a22      a 4500</xsl:text>
                </leader>
                <xsl:for-each select="Dados_marc/indicador">
                    <xsl:call-template name="buildMarcField"/>
                </xsl:for-each>
            </record>
        </collection>
    </xsl:template>

    <!--
    The template "buildMarcField" analizes the length of the "indicador".
    If it is equal to three, it means the tag is not repeatable. 
    If it is more than three, the tag is repeatable.

    If the MARC tag ("paragrafo") is lower then 009 it is a control field,
    if it is not, it is a datafield.
    -->

    <xsl:template name="buildMarcField">
        <!-- Main variables (begin) -->
        <xsl:variable name="tag" select="normalize-space(preceding-sibling::paragrafo[1])"/>
        <xsl:variable name="indicators" select="tokenize(., '&lt;br&gt; ')"/>
        <xsl:variable name="indicatorsLength" select="string-length(.)"/>
        <xsl:variable name="datafields"
            select="tokenize(normalize-space(./following-sibling::descricao[1]), ' &lt;br&gt;')"/>

        <!-- Main variables (end) -->
        <xsl:choose>
            <!-- 
            When the length is 3 and the "descricao" has ' &lt;br&gt;', it means there are 
            repeatable controlfield MARC tags, so we have to tokenize the content of the 
            "descricao" element.
            -->
            <xsl:when test="$indicatorsLength = 3">
                <xsl:choose>
                    <xsl:when test="number($tag) &lt; 9">
                        <xsl:choose>
                            <!-- For repeatable controlfields (006 and 007) -->
                            <xsl:when
                                test="contains(./following-sibling::descricao[1], ' &lt;br&gt;')">
                                <xsl:for-each select="$datafields">
                                    <xsl:variable name="position" select="position()"/>
                                    <controlfield xmlns="http://www.loc.gov/MARC21/slim">
                                        <xsl:attribute name="tag">
                                            <xsl:value-of select="$tag"/>
                                        </xsl:attribute>
                                        <xsl:value-of
                                            select="translate($datafields[$position], '#', ' ')"/>
                                    </controlfield>
                                </xsl:for-each>
                            </xsl:when>
                            <!-- For not repeatable controlfields (001, 003, 005 and 008) -->
                            <xsl:otherwise>
                                <controlfield xmlns="http://www.loc.gov/MARC21/slim">
                                    <xsl:attribute name="tag">
                                        <xsl:value-of select="$tag"/>
                                    </xsl:attribute>
                                    <xsl:value-of select="translate($datafields[1], '#', ' ')"/>
                                </controlfield>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <!-- For not repeatable datafields (fields greater than 009) -->
                    <xsl:otherwise>
                        <datafield xmlns="http://www.loc.gov/MARC21/slim">
                            <xsl:attribute name="tag">
                                <xsl:value-of select="$tag"/>
                            </xsl:attribute>
                            <xsl:attribute name="ind1">
                                <xsl:value-of select="replace($indicators, '(.)\s.', '$1')"/>
                            </xsl:attribute>
                            <xsl:attribute name="ind2">
                                <xsl:value-of select="replace($indicators, '.\s(.)', '$1')"/>
                            </xsl:attribute>
                            <xsl:for-each select="tokenize(substring($datafields, 2), '\$')">                              
                                <xsl:variable name="position" select="position()"/>
                                
                                <subfield>
                                    <xsl:attribute name="code">
                                        <xsl:value-of
                                            select="normalize-space(substring(.[1], 1, 1))"
                                        />
                                        
                                    </xsl:attribute>
                                    <xsl:value-of
                                        select="normalize-space(substring(.[1], 3))"
                                    />
                                </subfield>
                            </xsl:for-each>
                        </datafield>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <!-- For repeatable datafields (fields greater than 009) -->
            <xsl:when test="$indicatorsLength &gt; 3">
                <!-- 
                When the length is greater than 3, it means there are repeatable MARC tags, 
                so we have to tokenize the content of the "descricao" and "indicador" elements, 
                and match the tokens acording to their positions. Additionally, we must tokenize 
                each token of "descricao" in order to separate subfields.
                -->
                <xsl:for-each select="$indicators">
                    <xsl:variable name="position" select="position()"/>
                    <xsl:variable name="ind1">
                        <xsl:choose>
                            <xsl:when test="string-length(.) = 4">
                                <xsl:value-of select="replace(substring(., 1, 3), '(.)\s.', '$1')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="replace(., '(.)\s.', '$1')"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <xsl:variable name="ind2">
                        <xsl:choose>
                            <xsl:when test="string-length(.) = 4">
                                <xsl:value-of select="replace(substring(., 1, 3), '.\s(.)', '$1')"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="replace(., '.\s(.)', '$1')"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>
                    <datafield xmlns="http://www.loc.gov/MARC21/slim">
                        <xsl:attribute name="tag">
                            <xsl:value-of select="$tag"/>
                        </xsl:attribute>
                        <xsl:attribute name="ind1">
                            <xsl:value-of select="$ind1"/>
                        </xsl:attribute>
                        <xsl:attribute name="ind2">
                            <xsl:value-of select="$ind2"/>
                        </xsl:attribute>
                        <xsl:for-each
                            select="tokenize(substring(normalize-space($datafields[$position]), 2), '\$')">
                            <subfield>
                                <xsl:attribute name="code">
                                    <xsl:value-of select="normalize-space(substring(., 1, 1))"/>
                                </xsl:attribute>
                                <xsl:value-of select="normalize-space(substring(., 3))"/>
                            </subfield>
                        </xsl:for-each>
                    </datafield>
                </xsl:for-each>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
