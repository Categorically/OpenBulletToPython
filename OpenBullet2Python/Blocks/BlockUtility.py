from genericpath import isdir
import types
from OpenBullet2Python.Models.BotData import BotData
from enum import Enum
from OpenBullet2Python.LoliScript.LineParser import LineParser, ParseLabel, \
    ParseEnum, ParseLiteral, Lookahead, SetBool, ParseToken, \
    ParseInt, EnsureIdentifier
from OpenBullet2Python.Blocks.BlockBase import ReplaceValuesRecursive, \
    InsertVariable, ReplaceValues
from OpenBullet2Python.Models.CVar import CVar
from OpenBullet2Python.Models.CVar import VarType
from OpenBullet2Python.Functions.Conditions.Condition import Verify
from OpenBullet2Python.Functions.Conversion.Conversion import Conversion
from random import choice, shuffle
import os
from OpenBullet2Python.Functions.Files.Files import NotInCWD
from shutil import copyfile, move, rmtree

def string_escape(s, encoding='utf-8'):
    return (s.encode('latin1')
             .decode('unicode-escape')
             .encode('latin1')
             .decode(encoding))
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

    def FromLS(self, line:LineParser) -> None:
        if str(line.current).startswith("!"):
            return None

        self.group = ParseEnum(line)

        if self.group == UtilityGroup.List:

            self.list_name = ParseLiteral(line)
            self.list_action = ParseEnum(line)

            if self.list_action == ListAction.Join:
                self.Separator = ParseLiteral(line)

            elif self.list_action == ListAction.Sort:
                while Lookahead(line) == "Boolean":
                    boolean_name, boolean_value = SetBool(line,self)
                    
            elif self.list_action == ListAction.Map or \
                self.list_action == ListAction.Zip or \
                self.list_action == ListAction.Concat:
                self.SecondListName = ParseLiteral(line)

            elif self.list_action == ListAction.Add:
                self.ListItem = ParseLiteral(line)
                self.ListIndex = ParseLiteral(line)

            elif self.list_action == ListAction.Remove:
                self.ListIndex = ParseLiteral(line)

            elif self.list_action == ListAction.RemoveValues:
                self.ListElementComparer  = ParseEnum(line)
                self.ListComparisonTerm = ParseLiteral(line)
            else:
                pass

        elif self.group == UtilityGroup.Variable:
            self.VarName = ParseLiteral(line)
            self.var_action  = ParseEnum(line)
            if self.var_action == VarAction.Split:
                self.SplitSeparator = ParseLiteral(line)

        elif self.group == UtilityGroup.Conversion:
            self.ConversionFrom =ParseEnum(line)
            self.ConversionTo = ParseEnum(line)
            self.InputString = ParseLiteral(line)
        
        elif self.group == UtilityGroup.File:
            self.FilePath = ParseLiteral(line)
            self.file_action = ParseEnum(line)

            if self.file_action in [
                FileAction.Write, FileAction.WriteLines,
                FileAction.Append, FileAction.AppendLines,
                FileAction.Copy, FileAction.Move]:
                self.InputString = ParseLiteral(line)

        elif self.group == UtilityGroup.Folder:
            self.FolderPath = ParseLiteral(line)
            self.folder_action = ParseEnum(line)

        # Try to parse the arrow, otherwise just return the block as is with default var name and var / cap choice
        if not ParseToken(line,"Arrow",False,True):
            return self.Dict
            
        # Parse the VAR / CAP
        varType = ParseToken(line,"Parameter",True,True)
        if str(varType.upper()) == "VAR" or str(varType.upper()) == "CAP":
            if str(varType.upper()) == "CAP":
                self.Dict["IsCapture"] = True
                self.isCapture = True

        # Parse the variable/capture name
        VariableName = ParseToken(line,"Literal",True,True)
        self.VariableName = VariableName

    def Process(self, BotData):
        print(f"BLOCK: {self.block_type}, GROUP: {self.group}")

        replacedInput = ReplaceValues(self.InputString,BotData)
        if self.group == UtilityGroup.List:
            list1 = BotData.Variables.GetList(self.list_name) or []
            list2 = BotData.Variables.GetList(self.SecondListName) or []
            item = ReplaceValues(self.ListItem, BotData)
            index  = int(ReplaceValues(self.ListIndex, BotData))

            if self.list_action == ListAction.Create:
                output = list1
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
            
            file = ReplaceValues(self.FilePath, BotData)
            # If the file is not in the current dir, do nothing
            if NotInCWD(BotData.cwd, file) == True:
                print("File path is out of bounds")
                return

            if self.file_action == FileAction.Exists:
                output = os.path.isfile(file)
                BotData.Variables.Set(CVar(self.VariableName, str(output), self.isCapture))
            
            elif self.file_action == FileAction.Read:
                try:
                    with open(file, "r", errors="ignore") as f:
                        output = f.read()
                        BotData.Variables.Set(CVar(self.VariableName, str(output), self.isCapture))

                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.ReadLines:
                try:
                    with open(file, "r", errors="ignore") as f:
                        output = f.readlines()
                        BotData.Variables.Set(CVar(self.VariableName, output, self.isCapture))

                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.Write:
                try:
                    with open(file, "w", errors="ignore") as f:
                        f.write(string_escape(replacedInput))
                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.WriteLines:
                try:
                    with open(file, "w", errors="ignore") as f:
                        output = ReplaceValuesRecursive(self.InputString, BotData)
                        if type(output) == str:
                            f.writelines(string_escape(output))
                        elif type(output) == list:
                            f.writelines([string_escape(line) + "\n" for line in output])
                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.Append:
                try:
                    with open(file, "a", errors="ignore") as f:
                        f.write(string_escape(replacedInput))

                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.AppendLines:
                try:
                    with open(file, "a", errors="ignore") as f:
                        output = ReplaceValuesRecursive(self.InputString, BotData)
                        if type(output) == str:
                            f.writelines(string_escape(output))
                        elif type(output) == list:
                            f.writelines([string_escape(line) + "\n" for line in output])
                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.Copy:
                fileCopyLocation = ReplaceValues(self.InputString, BotData)
                if NotInCWD(BotData.cwd,fileCopyLocation) == True:
                    print("File path is out of bounds")
                    return
                try:
                    copyfile(file, fileCopyLocation)
                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.Move:
                fileMoveLocation = ReplaceValues(self.InputString, BotData)
                if NotInCWD(BotData.cwd,fileMoveLocation) == True:
                    print("File path is out of bounds")
                    return
                try:
                    move(file, fileMoveLocation)
                except Exception as e:
                    print(e)
                    return

            elif self.file_action == FileAction.Delete:
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    return
            print(f"Executed action {self.file_action} on file {file}")
        elif self.group == UtilityGroup.Folder:
            folder = ReplaceValues(self.FolderPath, BotData)
            if NotInCWD(BotData.cwd, folder):
                print("File path is out of bounds")
                return

            if self.folder_action == FolderAction.Exists:
                output = os.path.isdir(folder)
                BotData.Variables.Set(CVar(self.VariableName, str(output), self.isCapture))
                print(f"Executed action {self.folder_action} on file {folder}")

            elif self.folder_action == FolderAction.Create:
                if os.path.isdir(folder) == False:
                    os.mkdir(folder)
                    BotData.Variables.Set(CVar(self.VariableName, str(folder), self.isCapture))
                    print(f"Executed action {self.folder_action} on file {folder}")

            elif self.folder_action == FolderAction.Delete:
                if os.path.isdir(folder):
                    if input(f"Are you sure you want to remove \"{folder}\" [y/n]: ").lower() == "y":
                        rmtree(folder)
                        print(f"Executed action {self.folder_action} on file {folder}")