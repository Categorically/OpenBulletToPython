from os import replace
from OpenBullet2Python.Models.BotData import BotData
from enum import Enum
from OpenBullet2Python.LoliScript.LineParser import ParseLabel, \
    ParseEnum, ParseLiteral, line, Lookahead, SetBool, ParseToken, \
    ParseInt, EnsureIdentifier
from OpenBullet2Python.Blocks.BlockBase import ReplaceValuesRecursive, \
    InsertVariable, ReplaceValues
from OpenBullet2Python.Models.CVar import CVar
from OpenBullet2Python.Models.CVar import VarType
from OpenBullet2Python.Functions.Conditions.Condition import Verify
from OpenBullet2Python.Functions.Conversion.Conversion import Conversion

from random import choice, shuffle

class UtilityGroup(str, Enum):
    List = "List"
    Variable = "Variable"
    Conversion = "Conversion"
    File = "File"
    Folder = "Folder"

class VarAction(str, Enum):
    Split = "Split"

class ListAction(str, Enum):
    Create = "Create"
    Length = "Length"
    Join = "Join"
    Sort = "Sort"
    Concat = "Concat"
    Zip = "Zip"
    Map = "Map"
    Add = "Add"
    Remove = "Remove"
    RemoveValues = "RemoveValues"
    RemoveDuplicates = "RemoveDuplicates"
    Random = "Random"
    Shuffle = "Shuffle"

class FileAction(str, Enum):
    Exists = "Exists"
    Read = "Read"
    ReadLines = "ReadLines"
    Write = "Write"
    WriteLines = "WriteLines"
    Append = "Append"
    AppendLines = "AppendLines"
    Copy = "Copy"
    Move = "Move"
    Delete = "Delete"

class FolderAction(str, Enum):
    Exists = "Exists"
    Create = "Create"
    Delete = "Delete"
    
class BlockUtility:
    def __init__(self) -> None:
        self.Dict = {}
        # List
        self.list_name = None
        self.list_action = None
        # List Join
        self.Separator = None
        # List Sort
        self.Ascending = True
        # List Map
        self.SecondListName = None
        # List Add
        self.ListIndex = None
        self.ListItem = None
        # List Add, Remove
        self.ListIndex = "0"
        # List RemoveValues
        self.ListComparisonTerm = None
        self.ListElementComparer = None

        # Variable
        self.VarName = None
        self.var_action = None
        self.SplitSeparator = None

        # Conversion
        self.ConversionFrom = None
        self.ConversionTo = None

        # File
        self.file_action = None
        self.folder_action = None
        # Folder
        self.FolderPath = None

        self.InputString = ""

        # All
        self.isCapture = False
        self.group = None
        self.VariableName = ""

    def FromLS(self, input_line) -> None:
        input_line = input_line.strip()

        self.group = ParseEnum(line.current)

        if self.group == UtilityGroup.List:

            self.list_name = ParseLiteral(line.current)
            self.list_action = ParseEnum(line.current)

            if self.list_action == ListAction.Join:
                self.Separator = ParseLiteral(line.current)

            elif self.list_action == ListAction.Sort:
                while Lookahead(line.current) == "Boolean":
                    boolean_name, boolean_value = SetBool(line.current,self)
                    
            elif self.list_action == ListAction.Map or \
                self.list_action == ListAction.Zip or \
                self.list_action == ListAction.Concat:
                self.SecondListName = ParseLiteral(line.current)

            elif self.list_action == ListAction.Add:
                self.ListItem = ParseLiteral(line.current)
                self.ListIndex = ParseLiteral(line.current)

            elif self.list_action == ListAction.Remove:
                self.ListIndex = ParseLiteral(line.current)

            elif self.list_action == ListAction.RemoveValues:
                self.ListElementComparer  = ParseEnum(line.current)
                self.ListComparisonTerm = ParseLiteral(line.current)
            else:
                pass

        elif self.group == UtilityGroup.Variable:
            self.VarName = ParseLiteral(line.current)
            self.var_action  = ParseEnum(line.current)
            if self.var_action == VarAction.Split:
                self.SplitSeparator = ParseLiteral(line.current)

        elif self.group == UtilityGroup.Conversion:
            self.ConversionFrom =ParseEnum(line.current)
            self.ConversionTo = ParseEnum(line.current)
            self.InputString = ParseLiteral(line.current)
        
        elif self.group == UtilityGroup.File:
            self.FilePath = ParseLiteral(line.current)
            self.file_action = ParseEnum(line.current)

            if self.file_action == FileAction.Move:
                self.InputString = ParseLiteral(line.current)

        elif self.group == UtilityGroup.Folder:
            self.FolderPath = ParseLiteral(line.current)
            self.folder_action = ParseEnum(line.current)

        # Try to parse the arrow, otherwise just return the block as is with default var name and var / cap choice
        if not ParseToken(line.current,"Arrow",False,True):
            return self.Dict
            
        # Parse the VAR / CAP
        varType = ParseToken(line.current,"Parameter",True,True)
        if str(varType.upper()) == "VAR" or str(varType.upper()) == "CAP":
            if str(varType.upper()) == "CAP":
                self.Dict["IsCapture"] = True
                self.isCapture = True

        # Parse the variable/capture name
        VariableName = ParseToken(line.current,"Literal",True,True)
        self.VariableName = VariableName

    def Process(self, BotData):
        print(f"BLOCK: {self.block_type}, GROUP: {self.group}")

        replacedInput = ReplaceValues(self.InputString,BotData)
        if self.group == UtilityGroup.List:
            list1 = BotData.Variables.GetList(self.list_name)
            list2 = BotData.Variables.GetList(self.SecondListName)
            item = ReplaceValues(self.ListItem, BotData)
            index  = int(ReplaceValues(self.ListIndex, BotData))

            if self.list_action == ListAction.Create:
                output = ["1","2","3"]
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Create}, output: {output}")

            elif self.list_action == ListAction.Length:
                output = str(len(list1))
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Length}, output: {output}")

            elif self.list_action == ListAction.Join:
                output = self.Separator.join(list1)
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Join}, output: {output}")

            elif self.list_action == ListAction.Sort:
                output = sorted(list1)
                if not self.Ascending:
                    output = list(reversed(output))
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Sort}, output: {output}")

            elif self.list_action == ListAction.Concat:
                output = list1 + list2
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Concat}, output: {output}")
                
            elif self.list_action == ListAction.Zip:
                output = zip(list1, list2)
                output = [f"{a}{b}" for a, b in output]
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Zip}, output: {output}")

            elif self.list_action == ListAction.Map:
                output = zip(list1, list2)
                output = [{a: b} for a, b in output]
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Map}, output: {output}")

            elif self.list_action == ListAction.Add:
                variable = BotData.Variables.GetWithNameAndType(self.list_name, VarType.List)
                if not variable: return

                if len(variable.Value) == 0: index = 0
                elif index < 0: index += len(variable.Value)
                variable.Value.insert(index, item)

                print(f"ACTION: {ListAction.Add}, output: {variable.Value}")

            elif self.list_action == ListAction.Remove:
                variable = BotData.Variables.GetWithNameAndType(self.list_name, VarType.List)
                if not variable: return

                if len(variable.Value) == 0: index = 0
                elif index < 0: index += len(variable.Value)
                variable.Value.pop(index)

                print(f"ACTION: {ListAction.Remove}, output: {variable.Value}")

            elif self.list_action == ListAction.RemoveValues:
                output = [l for l in list1 if not Verify(
                    ReplaceValues(l, BotData), self.ListElementComparer, self.ListComparisonTerm
                )] 
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.RemoveValues}, output: {output}")

            elif self.list_action == ListAction.RemoveDuplicates:
                output = list(dict.fromkeys(list1))
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.RemoveDuplicates}, output: {output}")

            elif self.list_action == ListAction.Random:
                output = choice(list1)
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Random}, output: {output}")

            elif self.list_action == ListAction.Shuffle:
                output = list1
                shuffle(output)
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"ACTION: {ListAction.Shuffle}, output: {output}")

        elif self.group == UtilityGroup.Variable:

            if self.var_action == VarAction.Split:
                single = BotData.Variables.GetSingle(self.VarName)
                output = single.split(
                    ReplaceValues(self.SplitSeparator, BotData)
                )
                BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))
                print(f"Executed action {self.var_action} on variable {self.VarName} with outcome {output}")


        elif self.group == UtilityGroup.Conversion:
            conversionInputBytes = Conversion().ConvertFrom(replacedInput,self.ConversionFrom)
            conversionResult  = Conversion().ConvertTo(conversionInputBytes,self.ConversionTo)
            BotData.Variables.Set(CVar(self.VariableName, conversionResult, self.isCapture))
            print(f"Executed conversion {self.ConversionFrom} to {self.ConversionTo} on input {replacedInput} with outcome {conversionResult}")

        elif self.group == UtilityGroup.File:

            if self.file_action == FileAction.Exists:
                pass
            
            elif self.file_action == FileAction.Read:
                pass

            elif self.file_action == FileAction.ReadLines:
                pass

            elif self.file_action == FileAction.Write:
                pass

            elif self.file_action == FileAction.WriteLines:
                pass

            elif self.file_action == FileAction.Append:
                pass

            elif self.file_action == FileAction.AppendLines:
                pass

            elif self.file_action == FileAction.Copy:
                pass

            elif self.file_action == FileAction.Move:
                pass

            elif self.file_action == FileAction.Delete:
                pass

        elif self.group == UtilityGroup.Folder:

            if self.folder_action == FolderAction.Exists:
                pass

            elif self.folder_action == FolderAction.Create:
                pass

            elif self.folder_action == FolderAction.Delete:
                pass