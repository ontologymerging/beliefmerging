'''
def do_calculation(number1, number2):
    return number1 + number2
'''
import itertools




def PositionOfString(letterToFind,conceptstring):
    count=0
    for i in conceptstring:
        count=count+1
        if(letterToFind == i):
            return count
    return 0

def closure(relation, left, right, primaryConcept,listOfInterpretation):
    result=[]
    result = listOfInterpretation
    LeftInterpretation=[]
    RightInterpretation=[]
    positionRight = PositionOfString(right, primaryConcept) - 1
    positionLeft = PositionOfString(left, primaryConcept) - 1

    if relation=="->":
        LeftInterpretation.extend(listOfInterpretation[positionLeft])
        RightInterpretation.extend(listOfInterpretation[positionLeft])

    if relation=="<-":
        LeftInterpretation.extend(listOfInterpretation[positionRight])
        RightInterpretation.extend(listOfInterpretation[positionRight])

    if relation=="=":
        LeftInterpretation.extend(listOfInterpretation[positionRight])
        RightInterpretation.extend(listOfInterpretation[positionRight])
        LeftInterpretation.extend(listOfInterpretation[positionLeft])
        RightInterpretation.extend(listOfInterpretation[positionLeft])

    result[positionLeft].extend(LeftInterpretation)
    result[positionRight].extend(RightInterpretation)
    return result;

def Aggeration_Axioms(Axiom_Left, Axiom_Right,primaryConcept):
    for i in range(0,len(primaryConcept)):
        Axiom_Left[i].extend(Axiom_Right[i])
        #Remove concepts duplication
        Axiom_Left[i]=list(dict.fromkeys(Axiom_Left[i]))
    return Axiom_Left

def Abbreviation(Concept,primaryConcept):
    for i in range(0,len(primaryConcept)):
        Concept[i]=list(dict.fromkeys(Concept[i]))
        #Sorting asc
        Concept[i].sort()
    return Concept

def GetFather(Concept):
    Left=Concept[0]
    Relation = Concept[1]
    Right = Concept[2]

    if Relation=="->":
        return Right
    if Relation=="<-":
        return Left
    return Left

def GetChild(Concept):
    Left=Concept[0]
    Relation = Concept[1]
    Right = Concept[2]

    if Relation=="->":
        return Left
    if Relation=="<-":
        return Right
    return Left

def LeftSide(Concept):
    return Concept[0]

def RelationOfConcepts(Concept):
    return Concept[1]

def RightSide(Concept):
    return Concept[2]

def TransitionBetweenConcepts(ListConcept):
    Concept1=ListConcept[0]
    Concept2 = ListConcept[1]
    if GetChild(Concept1) == GetFather(Concept2) or GetFather(Concept1)== GetChild(Concept2):
        return True
    if RelationOfConcepts(Concept1)=="=" or RelationOfConcepts(Concept2)=="=":
        return True
    return False

def GenerateConcepts(InputAtomicConcepts, SubsumptionRole):
    AtomicConcepts = itertools.combinations(InputAtomicConcepts, 2)
    ListOfConcepts = []
    for concept in AtomicConcepts:
        for predicate in SubsumptionRole:
            EachConcepts = concept[0], predicate, concept[1]
            ListOfConcepts.append(EachConcepts)
    return ListOfConcepts

def PrintList(List):
    html=""
    for element in List:
        html="%s<li> %s</li>"%(html, element)
    html="<ol type='1'> %s </ol>"%html
    return html

def Combinations(ListOfConcepts):
    return itertools.combinations(ListOfConcepts,2)

def StrutureOfConcept(GenerateAxiom):
    ConceptsStructure = []
    for atomicConcepts in GenerateAxiom:
        Concept1 = atomicConcepts[0]
        Concept2 = atomicConcepts[1]
        if (LeftSide(Concept1) == LeftSide(Concept2) and RightSide(Concept1) == RightSide(Concept2)):
            continue
        else:
            pass
        if (RelationOfConcepts(Concept1) == RelationOfConcepts(Concept2)) and (
                RelationOfConcepts(Concept1) == "=") and (RightSide(Concept1) != RightSide(Concept2)):
            continue
        else:
            ConceptsStructure.append(atomicConcepts)
    return GenerateAxiom



def FindFather_AtMost(LeftConcept, RightConcept):
    if RelationOfConcepts(LeftConcept) == "=" and RelationOfConcepts(RightConcept) == "=":
        return GetFather(RightConcept)
    if RelationOfConcepts(LeftConcept) == "=":
        return GetFather(RightConcept)
    if RelationOfConcepts(RightConcept) == "=":
        return GetFather(LeftConcept)
    if  GetChild(LeftConcept)==GetFather(RightConcept):
        return GetFather(LeftConcept)
    if GetFather(LeftConcept) == GetChild(RightConcept):
        return GetFather(RightConcept)

def FindChild_AtLeast(LeftConcept, RightConcept):
    if RelationOfConcepts(LeftConcept) == "=" and RelationOfConcepts(RightConcept) == "=":
        return RightSide(RightConcept)
    if RelationOfConcepts(LeftConcept) == "=" :
        return GetChild(RightConcept)
    if RelationOfConcepts(RightConcept) == "=":
        return GetChild(LeftConcept)
    if  GetFather(LeftConcept)==GetChild(RightConcept):
        return GetChild(LeftConcept)
    if GetChild(LeftConcept) == GetFather(RightConcept):
        return GetChild(RightConcept)

def FindMax_ElementRanking(Concept1, Concept2, Interpretations,primaryConcept):

    if RelationOfConcepts(Concept1)=="=":
        positionRight = PositionOfString(RightSide(Concept1), primaryConcept) - 1
        positionLeft = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
        if(len(Interpretations[positionLeft])>=len(Interpretations[positionRight])):
            return LeftSide(Concept1), RightSide(Concept1)
        else:
            return RightSide(Concept1), LeftSide(Concept1)
    else:
        if RelationOfConcepts(Concept2)=="=":
            positionRight = PositionOfString(RightSide(Concept2), primaryConcept) - 1
            positionLeft = PositionOfString(LeftSide(Concept2), primaryConcept) - 1
            if (len(Interpretations[positionLeft]) >= len(Interpretations[positionRight])):
                return LeftSide(Concept2),  RightSide(Concept2)
            else:
                return RightSide(Concept2),LeftSide(Concept2)

def Initiation():
    A = ['a']
    B = ['b']
    C = ['c']
    Array_Interpretation = []
    Array_Interpretation.append(A)
    Array_Interpretation.append(B)
    Array_Interpretation.append(C)
    return Array_Interpretation

def CheckCorrectionOfInterpretation(Concept1, Concept2, Interpretations,primaryConcept):

    resultChecking_Concept1= False
    resultChecking_Concept2 = False
    #-----------------------Concept 1--------------------------------
    positionRight_1 = PositionOfString(RightSide(Concept1), primaryConcept) - 1
    positionLeft_1 = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
    # Considering Concept1
    if  RelationOfConcepts(Concept1)=="=":
        #Considering Interpretation regarding  Concept1
        if len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]): #Test each element of Left and Right Concept
            if all([Interpretations[positionLeft_1][i] == Interpretations[positionRight_1][i] for i in range(len(Interpretations[positionRight_1]))])==True:
                resultChecking_Concept1= True
        #print("Concept1 - Role =:", resultChecking_Concept1)

    if RelationOfConcepts(Concept1) == "->":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))])==True and Interpretations[positionLeft_1].count(Initiation()[positionRight_1][0])==0:
            resultChecking_Concept1 = True
        #print("Concept1 - Role ->:", resultChecking_Concept1)

    if RelationOfConcepts(Concept1) == "<-":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))])==True and Interpretations[positionRight_1].count(Initiation()[positionLeft_1][0])==0:
            resultChecking_Concept1 = True
        #print("Concept1 - Role <-:", resultChecking_Concept1)
    # -----------------------Concept 2--------------------------------
    positionRight_2 = PositionOfString(RightSide(Concept2), primaryConcept) - 1
    positionLeft_2 = PositionOfString(LeftSide(Concept2), primaryConcept) - 1
    #Considering Concept2
    if  RelationOfConcepts(Concept2)=="=":
        #Considering Interpretation regarding  Concept1
        if len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]): #Test each element of Left and Right Concept
            if all([Interpretations[positionLeft_2][i] == Interpretations[positionRight_2][i] for i in range(len(Interpretations[positionRight_2]))])==True:
                resultChecking_Concept2= True
        #print("Concept1 - Role =:", resultChecking_Concept2)

    if RelationOfConcepts(Concept2) == "->":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True and Interpretations[positionLeft_2].count(Initiation()[positionRight_2][0]) == 0:
            resultChecking_Concept2 = True
        #print("Concept1 - Role ->:", resultChecking_Concept2)

    if RelationOfConcepts(Concept2) == "<-":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True and Interpretations[positionRight_2].count( Initiation()[positionLeft_2][0]) == 0:
            resultChecking_Concept2 = True
        #print("Concept2 - Role <-:", resultChecking_Concept2)

    return all([resultChecking_Concept1,resultChecking_Concept2])

def Equal(A):
    B=[]
    for i in A:
        B.append(i)
    return B

def Initiation_ListElement(i):
    InterpretationCaseOfConcept1 = [
        [['a'], ['b'], ['c']],
        [['a'], [], []],
        [[], ['b'], []],
        [[], [], ['c']],
        [['a'], ['b'], []],
        [[], ['b'], ['c']],
        [['a'], [], ['c']],

    ]
    InterpretationCaseOfConcept = [
        [['a'], ['b'], ['c']],
    ]
    return InterpretationCaseOfConcept[i]

def FindEmpty_InConcept(Interpretations):
    for i in range(len(Interpretations)):
        if not Interpretations[i]:
            return True
    return False

def FindInterpretation_Subsumption(ConceptsStructure,InputAtomicConcepts,dem):
    #InterPre = [['a','c'], ['b'], ['a','c']]
    Array_All_Interpretation=[]

    Array_Init_Interpretation1=[]
    Array_Init_Interpretation2=[]
    for eachConcept in ConceptsStructure:
        Concept1 = eachConcept[0]
        Concept2 = eachConcept[1]
        # Show Conept1 and concept2 --> print(Concept1,"---",Concept2)
        dem = dem + 1
        print(dem, eachConcept)



        for i in range(7):
            Array_Init_Interpretation1 = Initiation_ListElement(i)
            Array_Init_Interpretation2 = Initiation_ListElement(i)

            Interpretation1_Left = closure(RelationOfConcepts(Concept1), LeftSide(Concept1), RightSide(Concept1),
                                           InputAtomicConcepts, Array_Init_Interpretation1)
            Interpretation2_Right = closure(RelationOfConcepts(Concept2), LeftSide(Concept2), RightSide(Concept2),
                                            InputAtomicConcepts, Array_Init_Interpretation2)
            InterpretationsOfConcepts = Aggeration_Axioms(Interpretation1_Left, Interpretation2_Right, InputAtomicConcepts)
            #print(InterpretationsOfConcepts)

            # Considering for transition between 02 Concepts
            Result_Interpretation = []
            if TransitionBetweenConcepts(eachConcept):
                #print("Transitive")
                Result_Interpretation = closure("->", FindChild_AtLeast(Concept1, Concept2),
                                                FindFather_AtMost(Concept1, Concept2),
                                                InputAtomicConcepts, InterpretationsOfConcepts)
            else:
                Result_Interpretation = InterpretationsOfConcepts
            FinalResultInterpretation = Abbreviation(Result_Interpretation, InputAtomicConcepts)
            # print(FinalResultInterpretation)

            if RelationOfConcepts(Concept1) == "=" or RelationOfConcepts(Concept2) == "=":
                MaxRanking = FindMax_ElementRanking(Concept1, Concept2, FinalResultInterpretation, InputAtomicConcepts)
                MaxRankingInterpretation = closure("->", MaxRanking[0], MaxRanking[1], InputAtomicConcepts,
                                                   FinalResultInterpretation)
                FinalResultInterpretation = Abbreviation(MaxRankingInterpretation, InputAtomicConcepts)

            print(FinalResultInterpretation)




            Array_All_Interpretation.append(FinalResultInterpretation)
            #print(InterPre)
            #rint(CheckCorrectionOfInterpretation(Concept1, Concept2,InterPre, InputAtomicConcepts))
        print("---------------------------------")



    return Array_All_Interpretation

def Init():
    A = []
    B = []
    C = []
    A.append(value_A.get())
    B.append(value_B.get())
    C.append(value_C.get())
    Temp = []
    Temp.append(A)
    Temp.append(B)
    Temp.append(C)
    return Temp

def FindClosureConcept(ConceptsStructure,InputAtomicConcepts):
    Temp=[]

    for eachConcept in ConceptsStructure:
        Concept1 = eachConcept[0]
        Concept2 = eachConcept[1]

        Array_1 = Init()
        Array_2 = Init()

        Interpretation1_Left = closure(RelationOfConcepts(Concept1), LeftSide(Concept1), RightSide(Concept1), InputAtomicConcepts, Array_1)
        Interpretation2_Right = closure(RelationOfConcepts(Concept2), LeftSide(Concept2), RightSide(Concept2),
                                            InputAtomicConcepts, Array_2)
        InterpretationsOfConcepts = Aggeration_Axioms(Interpretation1_Left, Interpretation2_Right, InputAtomicConcepts)
        if TransitionBetweenConcepts(eachConcept):
            # print("Transitive")
            Result_Interpretation = closure("->", FindChild_AtLeast(Concept1, Concept2),
                                                FindFather_AtMost(Concept1, Concept2),
                                                InputAtomicConcepts, InterpretationsOfConcepts)
        else:
            Result_Interpretation = InterpretationsOfConcepts

        FinalResultInterpretation = Abbreviation(Result_Interpretation, InputAtomicConcepts)

        if RelationOfConcepts(Concept1) == "=" or RelationOfConcepts(Concept2) == "=":
            MaxRanking = FindMax_ElementRanking(Concept1, Concept2, FinalResultInterpretation, InputAtomicConcepts)
            MaxRankingInterpretation = closure("->", MaxRanking[0], MaxRanking[1], InputAtomicConcepts,
                                                   FinalResultInterpretation)
            FinalResultInterpretation = Abbreviation(MaxRankingInterpretation, InputAtomicConcepts)
        Temp.append(FinalResultInterpretation)
    return Temp

def write_Considering_03_Ontology(ConceptsStructure, value1, value2, value3):
    Temp = "%d %d %d"%(int(value1),int(value2),int(value3))
    count = 0
    #Temp= "%s"%ConceptsStructure[1]

    #Temp = "%d. %s\n%d. %s\n%d. %s" % (int(value_1),ConceptsStructure[int(value_1)],int(value_2),ConceptsStructure[int(value_2)],int(value_3),ConceptsStructure[int(value_3)])
    """
    TempArray_ConceptStructure=[]
    TempArray_ConceptStructure.append(ConceptsStructure[int(value_1)-1])
    TempArray_ConceptStructure.append(ConceptsStructure[int(value_2)-1])
    TempArray_ConceptStructure.append(ConceptsStructure[int(value_3)-1])
    count=0
    Temp_Array_All_Interpretation = FindInterpretation_Subsumption(TempArray_ConceptStructure, InputAtomicConcepts, count)
    Temp_Array_Temporary = Equal(Temp_Array_All_Interpretation)
    for element in Temp_Array_All_Interpretation:
        if FindEmpty_InConcept(element):
            Temp_Array_Temporary.remove(element)
    #print(Temp_Array_Temporary)
    count=0
    for i in Temp_Array_Temporary:
        count=count+1
        Temp = "%s\n%d. %s"%(Temp,count,i)
    Temp="%s\n"%Temp
    #======================== for Checking =======================
    CountID = 0
    CountTrue = 0
    CountFalse = 0
    for eachConcept in TempArray_ConceptStructure:
        Concept1 = eachConcept[0]
        Concept2 = eachConcept[1]
        CountID = CountID + 1
        Temp = "%s\n%d. %s"%(Temp,CountID, eachConcept)

        CountTrue = 0
        CountFalse = 0

        for eachInterpretation in Temp_Array_Temporary:
            # print(eachInterpretation, CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts))
            if (CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts) == True):
                CountTrue = CountTrue + 1
            else:
                CountFalse = CountFalse + 1
#       print("True:", CountTrue, "--", "False:", CountFalse)
        Temp = "%s\nTrue: %d. False: %d\n" % (Temp, CountTrue, CountFalse)
    """
    return "Closure Of Concepts %s" % Temp

#===============================================================================================================================

def CheckCorrectionOfInterpretation_EachFormular(Concept1, Concept2, Interpretations,primaryConcept):

    resultChecking_Concept1= False
    resultChecking_Concept2 = False
    #-----------------------Concept 1--------------------------------
    positionRight_1 = PositionOfString(RightSide(Concept1), primaryConcept) - 1
    positionLeft_1 = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
    positionRight_2 = PositionOfString(RightSide(Concept2), primaryConcept) - 1
    positionLeft_2 = PositionOfString(LeftSide(Concept2), primaryConcept) - 1

    if RelationOfConcepts(Concept1) == "<-":
        if LeftSide(Concept1)==LeftSide(Concept2):
            if RelationOfConcepts(Concept2)=="->":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True\
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True\
                        and Interpretations[positionRight_1]==Initiation()[positionRight_1]\
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2]\
                        and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]: #b in bottom
                    resultChecking_Concept1= True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True\
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True\
                        and Interpretations[positionRight_1]==Initiation()[positionRight_1] \
                        and Interpretations[positionRight_2] == Initiation()[positionRight_2]:  # b in bottom:
                    resultChecking_Concept1=True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True \
                         and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True\
                         and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]) \
                         and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]:  # b in bottom

                    resultChecking_Concept1=True
        else:
            if RelationOfConcepts(Concept2) == "->":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True \
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True \
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2] \
                        and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]:  # b in bottom
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in
                                 range(len(Interpretations[positionRight_2]))]) == True \
                        and Initiation()[positionLeft_2][0] not in Interpretations[positionRight_2] \
                        and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]:  # b in bottom
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2])\
                        and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]:
                    resultChecking_Concept1 = True

    #===============================================================================
    #----------------------------   --->    ----------------------------------------
    # ===============================================================================

    if RelationOfConcepts(Concept1) == "->":
        if LeftSide(Concept1) == LeftSide(Concept2):
            if RelationOfConcepts(Concept2) == "->":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True \
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2] \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in botto
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and Initiation()[positionLeft_2][0] not in Interpretations[positionRight_2] \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in bottom
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]) \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in bottom
                    resultChecking_Concept1 = True
        else:
            if RelationOfConcepts(Concept2) == "->":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True \
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2] \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in botto
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and Initiation()[positionLeft_2][0] not in Interpretations[positionRight_2] \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in bottom
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]) \
                        and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]:  # b in bottom
                    resultChecking_Concept1 = True
    # ===============================================================================
    # ----------------------------   --->    ----------------------------------------
    # ===============================================================================
    if RelationOfConcepts(Concept1) == "=":
        if LeftSide(Concept1) == LeftSide(Concept2):
            if RelationOfConcepts(Concept2) == "->":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                    and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True \
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2]:
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and Initiation()[positionLeft_2][0] not in Interpretations[positionRight_2]:
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]):
                    resultChecking_Concept1 = True
        else:
            if RelationOfConcepts(Concept2) == "->":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                    and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and all([Interpretations[positionLeft_2][i] in Interpretations[positionRight_2] for i in range(len(Interpretations[positionLeft_2]))]) == True \
                        and Initiation()[positionRight_2][0] not in Interpretations[positionLeft_2]:
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "<-":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and all([Interpretations[positionRight_2][i] in Interpretations[positionLeft_2] for i in range(len(Interpretations[positionRight_2]))]) == True \
                        and Initiation()[positionLeft_2][0] not in Interpretations[positionRight_2]:
                    resultChecking_Concept1 = True
            if RelationOfConcepts(Concept2) == "=":
                if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                        and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]) \
                        and len(Interpretations[positionLeft_2]) == len(Interpretations[positionRight_2]):
                    resultChecking_Concept1 = True

    return resultChecking_Concept1

#==============================================================================================================================




def CheckCorrectionOfInterpretation_EachConcept(Concept1, Interpretations,primaryConcept):
    '''
    resultChecking_Concept1= False
    #-----------------------Concept 1--------------------------------
    positionRight_1 = PositionOfString(RightSide(Concept1), primaryConcept) - 1
    positionLeft_1 = PositionOfString(LeftSide(Concept1), primaryConcept) - 1
    # Considering Concept1
    if  RelationOfConcepts(Concept1)=="=":
        #Considering Interpretation regarding  Concept1
        if len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]): #Test each element of Left and Right Concept
            if all([Interpretations[positionLeft_1][i] == Interpretations[positionRight_1][i] for i in range(len(Interpretations[positionRight_1]))])==True:
                resultChecking_Concept1= True
        #print("Concept1 - Role =:", resultChecking_Concept1)

    if RelationOfConcepts(Concept1) == "->":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))])==True and Interpretations[positionLeft_1].count(Initiation()[positionRight_1][0])==0:
            resultChecking_Concept1 = True
        #print("Concept1 - Role ->:", resultChecking_Concept1)


    if RelationOfConcepts(Concept1) == "<-":
        # Considering Interpretation regarding  Concept1
        if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))])==True and Interpretations[positionRight_1].count(Initiation()[positionLeft_1][0])==0:
            resultChecking_Concept1 = True
        #print("Concept1 - Role <-:", resultChecking_Concept1)
    return resultChecking_Concept1;
    '''
    resultChecking_Concept1 = False
    # -----------------------Concept 1--------------------------------
    positionRight_1 = PositionOfString(RightSide(Concept1), primaryConcept) - 1
    positionLeft_1 = PositionOfString(LeftSide(Concept1), primaryConcept) - 1

    if RelationOfConcepts(Concept1) == "<-":
        if all([Interpretations[positionRight_1][i] in Interpretations[positionLeft_1] for i in range(len(Interpretations[positionRight_1]))]) == True \
                and Initiation()[positionLeft_1][0] not in Interpretations[positionRight_1]: #b in bottom
            resultChecking_Concept1 = True
    if RelationOfConcepts(Concept1) == "->":
        if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                and Initiation()[positionRight_1][0] not in Interpretations[positionLeft_1]: #b in bottom
            resultChecking_Concept1 = True
    if RelationOfConcepts(Concept1) == "=":
        if all([Interpretations[positionLeft_1][i] in Interpretations[positionRight_1] for i in range(len(Interpretations[positionLeft_1]))]) == True \
                and len(Interpretations[positionLeft_1]) == len(Interpretations[positionRight_1]):
            resultChecking_Concept1 = True

    return resultChecking_Concept1

#----------------------------------------------------------
#----------------------BUTTON-----------------------

