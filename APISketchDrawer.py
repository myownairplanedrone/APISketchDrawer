import sys

from FreeCAD    import *
#from App        import *
#from Part       import *
#from PartDesign import *
#from Sketcher   import *

# DrawGeometries
# ConvertGeometriesIntoSVGPath
# ConvertSVGPathIntoGeometries

def DrawGeometries(iGeometries, iSketch = None, iBody = None, iPart = None, iDocument = None):
   aDrawGeometriesClass = GeometriesMaker("DrawGeometries", iGeometries, iSketch, iBody, iPart, iDocument)
   return aDrawGeometriesClass.Parse()

class GeometriesMaker:
   def __init__(self, iFunctionName, iGeometries, iSketch, iBody, iPart, iDocument):
      self.__caller_function  = iFunctionName
      self.__input_geometries = iGeometries
      self.__input_sketch     = iSketch
      self.__input_body       = iBody
      self.__input_part       = iPart
      self.__input_document   = iDocument
      self.__geometries       = None
      self.__sketch           = None
      self.__body             = None
      self.__part             = None
      self.__document         = None

   def Parse(self):
      if self.__ValidateParameters() is False:
         return False
      self.__GetDocument()
      self.__GetSketch()
      self.__GetPart()
      self.__GetBody()
      if self.__CreateMissingObjects() is False:
         return False
      return True

   def __ValidateParameters(self):
      if not isinstance(self.__input_document, (type(None), str)) and not hasattr(self.__input_document, "TypeId") and self.__input_document.TypeId != "App::Document":
         print("ERROR: {}: Param #5: Parameter 'iDocument' must be either 'None', a string ('str') or a Document class ('App::Document'). Instead, got type '{}'".format(self.__caller_function, type(self.__input_document)))
         return False
      if not isinstance(self.__input_part    , (type(None), str)) and not hasattr(self.__input_document, "TypeId") and self.__input_document.TypeId != "App::Part":
         print("ERROR: {}: Param #4: Parameter 'iPart' must be either 'None', a string ('str') or a Part class ('App::Part'). Instead, got type '{}'".format(self.__caller_function, type(self.__input_part)))
         return False
      if not isinstance(self.__input_body    , (type(None), str)) and not hasattr(self.__input_document, "TypeId") and self.__input_document.TypeId != "PartDesign::Body":
         print("ERROR: {}: Param #3: Parameter 'iBody' must be either 'None', a string ('str') or a Body class ('PartDesign::Body'). Instead, got type '{}'".format(self.__caller_function, type(self.__input_body)))
         return False
      if not isinstance(self.__input_sketch  , (type(None), str)) and not hasattr(self.__input_document, "TypeId") and self.__input_document.TypeId != "Sketcher::SketchObject":
         print("ERROR: {}: Param #2: Parameter 'iSketch' must be either 'None', a string ('str') or a Sketcher class ('Sketcher::SketchObject'). Instead, got type '{}'".format(self.__caller_function, type(self.__input_sketch)))
         return False
      if not isinstance(self.__input_geometries, str):
         print("ERROR: {}: Param #1: Parameter 'iGeometries' must be a string ('str'). Instead, got type '{}'".format(self.__caller_function, type(self.__input_geometries)))
         return False
      return True

   def __GetDocument(self):
      self.__document = None
      if isinstance(self.__input_document, str):
         try:
            aListOfDocumentsName = App.listDocuments()
         except:
            print("ERROR: {}: Failed to get the list of opened documents in FreeCAD.".format(self.__caller_function))
            aListOfDocumentsName = []
         for aDocumentName in aListOfDocumentsName:
            if len(aDocumentName) > 0 and aDocumentName == self.__input_document:
               self.__document = App.getDocument(aDocumentName)
               break
      if hasattr(self.__input_document, "TypeId") and isinstance(self.__input_document.TypeId, str) and self.__input_document.TypeId == "App::Document":
         self.__document = self.__input_document
      if isinstance(self.__input_document, type(None)):
         self.__document = App.activeDocument()

   def __GetPart(self):
      self.__part = None
      if isinstance(self.__input_part, str) and self.__document is not None:
         for aObject in self.__document.Objects:
            if hasattr(aObject, "TypeId") and isinstance(aObject.TypeId, str) and aObject.TypeId == "App::Part":
               if hasattr(aObject, "Name"  ) and isinstance(aObject.Name  , str) and len(aObject.Name  ) > 0 and aObject.Name   == self.__input_part:
                  self.__part = aObject
                  break
               if hasattr(aObject, "Label" ) and isinstance(aObject.Label , str) and len(aObject.Label ) > 0 and aObject.Label  == self.__input_part:
                  self.__part = aObject
                  break
               if hasattr(aObject, "Label2") and isinstance(aObject.Label2, str) and len(aObject.Label2) > 0 and aObject.Label2 == self.__input_part:
                  self.__part = aObject
                  break
      if hasattr(self.__input_part, "TypeId") and isinstance(self.__input_part.TypeId, str) and self.__input_part.TypeId == "App::Part":
         self.__part = self.__input_part
      if isinstance(self.__input_part, type(None)):
         self.__part = None

   def __GetBody(self):
      self.__body = None
      if isinstance(self.__input_body, str) and self.__document is not None:
         for aObject in self.__document.Objects:
            if hasattr(aObject, "TypeId") and isinstance(aObject.TypeId, str) and aObject.TypeId == "PartDesign::Body":
               if hasattr(aObject, "Name"  ) and isinstance(aObject.Name  , str) and len(aObject.Name  ) > 0 and aObject.Name   == self.__input_part:
                  self.__body = aObject
                  break
               if hasattr(aObject, "Label" ) and isinstance(aObject.Label , str) and len(aObject.Label ) > 0 and aObject.Label  == self.__input_part:
                  self.__body = aObject
                  break
               if hasattr(aObject, "Label2") and isinstance(aObject.Label2, str) and len(aObject.Label2) > 0 and aObject.Label2 == self.__input_part:
                  self.__body = aObject
                  break
      if hasattr(self.__input_body, "TypeId") and isinstance(self.__input_body.TypeId, str) and self.__input_body.TypeId == "PartDesign::Body":
         self.__body = self.__input_body
      if isinstance(self.__input_body, type(None)):
         self.__body = None

   def __GetSketch(self):
      self.__sketch = None
      if isinstance(self.__input_sketch, str) and self.__document is not None:
         for aObject in self.__document.Objects:
            if hasattr(aObject, "TypeId") and isinstance(aObject.TypeId, str) and aObject.TypeId == "Sketcher::SketchObject":
               if hasattr(aObject, "Name"  ) and isinstance(aObject.Name  , str) and len(aObject.Name  ) > 0 and aObject.Name   == self.__input_part:
                  self.__sketch = aObject
                  break
               if hasattr(aObject, "Label" ) and isinstance(aObject.Label , str) and len(aObject.Label ) > 0 and aObject.Label  == self.__input_part:
                  self.__sketch = aObject
                  break
               if hasattr(aObject, "Label2") and isinstance(aObject.Label2, str) and len(aObject.Label2) > 0 and aObject.Label2 == self.__input_part:
                  self.__sketch = aObject
                  break
      if hasattr(self.__input_sketch, "TypeId") and isinstance(self.__input_sketch.TypeId, str) and self.__input_sketch.TypeId == "Sketcher::SketchObject":
         self.__sketch = self.__input_sketch
      if isinstance(self.__input_sketch, type(None)):
         self.__sketch = None

   def __CreateMissingObjects(self):
      #if isinstance(self.__document, type(None)):
      #   aAllOpenedDocuments = App.listDocuments()
      #   aDocumentNewDefaultPrefixName = "NewDocWithSketch"
      #   if aDocumentNewDefaultPrefixName not in aAllOpenedDocuments:
      #      self.__document = App.newDocument(aDocumentNewDefaultPrefixName)
      #   else:
      #      aCounter = 0
      #      while aDocumentNewDefaultPrefixName + str(aCounter) in aAllOpenedDocuments:
      #         aCounter = aCounter + 1
      #      self.__document = App.newDocument(aDocumentNewDefaultPrefixName + str(aCounter))
      return True


DrawGeometries("C", None, None, None, None)
