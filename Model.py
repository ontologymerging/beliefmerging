from flask import Flask, request

from processing import FindClosureConcept
from processing import Init
from processing import FindInterpretation_Subsumption
from processing import FindEmpty_InConcept
from processing import Initiation_ListElement
from processing import Equal
from processing import CheckCorrectionOfInterpretation
from processing import Initiation
from processing import FindMax_ElementRanking
from processing import FindChild_AtLeast
from processing import FindFather_AtMost
from processing import StrutureOfConcept
from processing import PrintList
from processing import GenerateConcepts
from processing import TransitionBetweenConcepts
from processing import RightSide
from processing import RelationOfConcepts
from processing import LeftSide
from processing import GetChild
from processing import GetFather
from processing import Abbreviation
from processing import Aggeration_Axioms
from processing import closure
from processing import PositionOfString
from processing import Combinations
from processing import write_Considering_03_Ontology
from processing import CheckCorrectionOfInterpretation_EachConcept


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = "chao moi nguoi nhe"


    Relations = "->","<-","="
    #Relations = "&#8549;","&#8550","="
    InputAtomicConcepts="ABC"
    ListOfConcepts=GenerateConcepts(InputAtomicConcepts,Relations)

    result_List = PrintList(ListOfConcepts)

    #Show list of concepts for 03 atomic concepts
    #print(ListOfConcepts)
    #print("---------------------------------")
    #Generating Axiom E.g: A->B and B->C,....
    GenerateAxiom1 = Combinations(ListOfConcepts)
    GenerateAxiom2 = Combinations(ListOfConcepts)
    #print("---------------------------------")



    #-------------------------------------------------------------------------

    #ConceptsStructure=StrutureOfConcept(GenerateAxiom2)
    ConceptsStructure = []
    for atomicConcepts in GenerateAxiom2:
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
    #--------------------------------------------------------------------------

    result_List3 = PrintList(ConceptsStructure)


    #---------------------------------------------------------
    print("---------------------------------")
    #result=[1,2,3]
    count=0
    Array_All_Interpretation = FindInterpretation_Subsumption(ConceptsStructure,InputAtomicConcepts,count)
    #PrintList(Array_All_Interpretation)

    countRong=0
    #Empty=[]

    Array_Temporary = Equal(Array_All_Interpretation)
    for element in Array_All_Interpretation:
        count = count + 1
        if FindEmpty_InConcept(element):
            countRong = countRong+1
            Array_Temporary.remove(element)

    print("Result of Empty Subset",countRong)


    Array_All_Interpretation = Equal(Array_Temporary)
    print("-----------------------------------")
    PrintList(ConceptsStructure)
    print("-----------------------------------")
    PrintList(Array_All_Interpretation)
    print("-----------------------------------")
    result_List2 = PrintList(Array_All_Interpretation)
    Array_All_Interpretation_1=[]
    for i  in Array_All_Interpretation:
        if i in Array_All_Interpretation_1:
            continue
        else:
            Array_All_Interpretation_1.append(i)

    result_List2_1 = PrintList(Array_All_Interpretation_1)
    #---------------- Checking Correction of Interpretation in 03 ONTOLOGIES----------------------
    Result_UnSatisfied_Interpre="<h5 style='text-align:center; color:#ff0000;'>Please input 03 ontologies and click the button \"COMPUTE\"</h5>"


    #---------------- Checking Correction of Interpretation in each Concept--------------------------
    html=""
    html_concept=""
    result_truefalse=""
    CountID=0
    CountTrue=0
    CountFalse=0
    result_Statistics=[]
    result_Statistics_03Ontologies=[]
    for eachConcept in ConceptsStructure:
        Concept1 = eachConcept[0]
        Concept2 = eachConcept[1]
        CountID=CountID+1
        html_concept="%s <li> %s"%(html_concept, eachConcept)
        #print(CountID,eachConcept)

        CountTrue = 0
        CountFalse = 0
        for eachInterpretation in Array_All_Interpretation:
            #print(eachInterpretation, CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts))
            if(CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts)==True):
                CountTrue=CountTrue+1
            else:
                CountFalse = CountFalse+1

        result_truefalse = "True: %s - False: %s "%(CountTrue, CountFalse)
        html_concept="%s <p style='color:red;'><b> %s</b></p> </li> "%(html_concept, result_truefalse)
        result_Statistics.append([CountTrue,CountFalse])

    html="<ol>%s</ol>"%html_concept
    result=""
    Content=""
    #---------------------------------------------------------------------


    if request.method == "POST": #POST
        number1 = None
        number2 = None
        number3 = None

        try:
            number1 = float(request.form["number1"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        try:
            number2 = float(request.form["number2"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])
        try:
            number3 = float(request.form["number3"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number3"])
        if number1 is not None and number2 is not None and number3 is not None:
            number=[]
            number.append(number1)
            number.append(number2)
            number.append(number3)
            result = "<h3 text-align='center'>Considering O%s, O%s, O%s</h3><hr/>"%(int(number1),int(number2),int(number3))
            TempArray_ConceptStructure=[]
            TempArray_ConceptStructure.append(ConceptsStructure[int(number1)-1])
            TempArray_ConceptStructure.append(ConceptsStructure[int(number2)-1])
            TempArray_ConceptStructure.append(ConceptsStructure[int(number3)-1])
            count=0

            Temp_Array_All_Interpretation = FindInterpretation_Subsumption(TempArray_ConceptStructure, InputAtomicConcepts, count)
            Temp_Array_Temporary = Equal(Temp_Array_All_Interpretation)
            for element in Temp_Array_All_Interpretation:
                if FindEmpty_InConcept(element):
                    Temp_Array_Temporary.remove(element)
            #print(Temp_Array_Temporary)


            #======================== for Checking =======================
            Content="<h4 style='text-align:center'>Consideration of interpretations of 03 Ontologies </h4>"
            CountID = 0
            CountTrue = 0
            CountFalse = 0
            for eachConcept in TempArray_ConceptStructure:
                Concept1 = eachConcept[0]
                Concept2 = eachConcept[1]

                Content = "%s <p><b>%d. %s </b></p"%(Content, number[CountID],eachConcept)
                CountID = CountID + 1
                CountTrue = 0
                CountFalse = 0

                for eachInterpretation in Temp_Array_Temporary:
                    # print(eachInterpretation, CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts))
                    if (CheckCorrectionOfInterpretation(Concept1, Concept2, eachInterpretation, InputAtomicConcepts) == True):
                        CountTrue = CountTrue + 1
                    else:
                        CountFalse = CountFalse + 1

                #result = "%s\nTrue: %d. False: %d\n" % (result, CountTrue, CountFalse)
                Content = "%s<br/><li>True: %s ,  False: %s</li>"%(Content, CountTrue,CountFalse)
                result_Statistics_03Ontologies.append([CountTrue,CountFalse])

            result="%s<p>%s</p>"%(result,Content)
            result="%s<hr/>"%(result)

            result="%s<h3>  O(%s) &nbsp &nbsp  O(%s) &nbsp &nbsp   O(%s)</h3>"%(result,int(number1), int(number2), int(number3))
            result="%s<h6> &nbsp- Combination between O(%s) and  O(%s)</h6>"%(result,int(number1), int(number2))
            result_combination1 = (float(result_Statistics_03Ontologies[0][0])+float(result_Statistics_03Ontologies[1][0]))/2
            result_combination2 = (float(result_combination1)+float(result_Statistics_03Ontologies[2][0]))/2


            Content=""
            Content="%s<h5 style='color:blue;'> Average(O(%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number1),int(result_Statistics_03Ontologies[0][0]),int(number2),int(result_Statistics_03Ontologies[1][0]),float(result_combination1))

            Content="%s<h6>  &nbsp- Combination between O(%s,%s) and  O(%s)</h6>"%(Content,int(number1), int(number2),int(number3))
            Content="%s<h5 style='color:blue;'> Average(O(%d,%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number1),int(number2),int(result_combination1),int(number3),int(result_Statistics_03Ontologies[2][0]),float(result_combination2))
            result="%s %s"%(result,Content)

            result="%s<hr/>"%(result)

            result_combination1 = (float(result_Statistics_03Ontologies[1][0])+float(result_Statistics_03Ontologies[2][0]))/2
            result_combination2 = (float(result_combination1)+float(result_Statistics_03Ontologies[0][0]))/2
            result="%s<h6> &nbsp- Combination between O(%s) and  O(%s)</h6>"%(result,int(number1), int(number2))

            Content=""
            Content="%s<h5 style='color:blue;'> Average(O(%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number2),int(result_Statistics_03Ontologies[1][0]),int(number3),int(result_Statistics_03Ontologies[2][0]),float(result_combination1))
            Content="%s<h6>  &nbsp- Combination between O(%s,%s) and  O(%s)</h6>"%(Content,int(number1), int(number2),int(number3))

            Content="%s<h5 style='color:blue;'> Average(O(%d,%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number2),int(number3),int(result_combination1),int(number1),int(result_Statistics_03Ontologies[0][0]),float(result_combination2))
            result="%s %s"%(result,Content)

            #----------------------------------Show Interpretation-----------------
            #Content=""
            #for i in Temp_Array_Temporary:
            #    count=count+1
            #    Content = "%s<li>%s</li>"%(Content, i)
            #result="%s<ol>%s</ol>"%(result,Content)
            #==========================================================

            result="%s<hr/>"%(result)
            result="%s<hr/>"%(result)
            #========================================================
            result="%s<h4 style='text-align:center'>Consideration of All Interpretations</h4>"%result
            Content=""
            Content="%s<li>%s. <p>True:%s, False: %s</p></li>"%(Content,ConceptsStructure[int(number1)-1], result_Statistics[int(number1)][0],result_Statistics[int(number1)][1])
            Content="%s<li>%s. <p>True:%s, False: %s</p></li>"%(Content,ConceptsStructure[int(number2)-1], result_Statistics[int(number2)][0],result_Statistics[int(number2)][1])
            Content="%s<li>%s. <p>True:%s, False: %s</p></li>"%(Content,ConceptsStructure[int(number3)-1],result_Statistics[int(number3)][0],result_Statistics[int(number3)][1])

            result="%s<ol>%s</ol>"%(result,Content)
            result="%s<hr/>"%(result)


            result="%s<h3>  O(%s) &nbsp &nbsp  O(%s) &nbsp &nbsp   O(%s)</h3>"%(result,int(number1), int(number2), int(number3))

            result_combination1 = (float(result_Statistics[int(number1)][0])+float(result_Statistics[int(number2)][0]))/2
            result_combination2 = (float(result_combination1)+float(result_Statistics[int(number3)][0]))/2

            result="%s<h6> &nbsp- Combination between O(%s) and  O(%s)</h6>"%(result,int(number1), int(number2))
            Content=""
            Content="%s<h5 style='color:blue;> Average(O(%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number1),int(result_Statistics[int(number1)][0]),int(number2),int(result_Statistics[int(number2)][0]),float(result_combination1))

            Content="%s<h6>  &nbsp- Combination between O(%s,%s) and  O(%s)</h6>"%(Content,int(number1), int(number2),int(number3))
            Content="%s<h5 style='color:blue;> Average(O(%d,%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number1),int(number2),int(result_combination1),int(number3),int(result_Statistics[int(number3)][0]),float(result_combination2))
            result="%s %s"%(result,Content)

            result="%s<hr/>"%(result)

            result_combination1 = (float(result_Statistics[int(number2)][0])+float(result_Statistics[int(number3)][0]))/2
            result_combination2 = (float(result_combination1)+float(result_Statistics[int(number1)][0]))/2

            result="%s<h6> &nbsp- Combination between O(%s) and  O(%s)</h6>"%(result,int(number1), int(number2))
            Content=""
            Content="%s<h5 style='color:blue;> Average(O(%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number2),int(result_Statistics[int(number2)][0]),int(number3),int(result_Statistics[int(number3)][0]),float(result_combination1))

            #Content="%s<h6>  &nbsp- Combination between O(%s,%s) and  O(%s)</h6>"%(Content,int(number1), int(number2),int(number3))
            Content="%s<h5 style='color:blue;> Average(O(%d,%d): %s, O(%d): %s) = %s</h5>"%(Content,int(number2),int(number3),int(result_combination1),int(number1),int(result_Statistics[int(number1)][0]),float(result_combination2))
            result="%s %s"%(result,Content)


            #========================================================================

            id=0
            h=0
            tang=0
            Sum_Interpretation=[]
            Sum_ThreeOntology=[]
            for i in ConceptsStructure:
                id=id+1
                for h in range(len(number)):
                    tang=0
                    if (id == number[h]):
                        print("%s", i)
                        for j in Array_All_Interpretation_1:
                            tang = tang + 1
                            countTrue = 0
                            countFalse = 0
                            #print("%s - %s"%(i,j))
                            #considering with unstatisfied formulars
                            if(CheckCorrectionOfInterpretation_EachConcept(i[0],j,InputAtomicConcepts)):
                                countTrue=countTrue+1
                            else:
                                countFalse = countFalse +1
                            if(CheckCorrectionOfInterpretation_EachConcept(i[1],j,InputAtomicConcepts)):
                                countTrue=countTrue+1
                            else:
                                countFalse = countFalse +1

                            #print("%s. %s -- %s"%(tang,countTrue, countFalse))
                            Sum_Interpretation.append(countFalse)

                        Sum_ThreeOntology.append(Sum_Interpretation)
                        Sum_Interpretation=[]


            List_Sum_ThreeOntologies=[]
            for i in range(len(Sum_ThreeOntology[0])):
                SumAll = Sum_ThreeOntology[0][i]+ Sum_ThreeOntology[1][i]+ Sum_ThreeOntology[2][i]
                List_Sum_ThreeOntologies.append(SumAll)
            Sum_ThreeOntology.append(List_Sum_ThreeOntologies)
            Sum_ThreeOntology.append(Array_All_Interpretation_1)

            #Vertical to horizontal in array
            Rotate_Array = [[Sum_ThreeOntology[j][i] for j in range(len(Sum_ThreeOntology))] for i in range(len(Sum_ThreeOntology[0]))]
            Rotate_Array.sort(key=lambda Rotate_Array: Rotate_Array[3])#,reverse=True)
            Number_Sorted_Array=[]
            Number_Sorted_Array.append(int(number1))
            Number_Sorted_Array.append(int(number2))
            Number_Sorted_Array.append(int(number3))
            Number_Sorted_Array.sort()
            Result_UnSatisfied_Interpre='''<h5 style="text-align: center;">O{0} - {1}</h5><h5 style="text-align: center;">O{2} - {3}</h5><h5 style="text-align: center;">O{4} - {5}</h5>'''.format(Number_Sorted_Array[0],ConceptsStructure[int(Number_Sorted_Array[0])-1],Number_Sorted_Array[1],ConceptsStructure[int(Number_Sorted_Array[1])-1],Number_Sorted_Array[2],ConceptsStructure[int(Number_Sorted_Array[2])-1])
            Result_UnSatisfied_Interpre='''%s
                    <table align="center"  style='font-size:13px;'>
                    <tr>
                        <th> Id </th>
                        <th> List of Interpretation </th>
                        <th align='center'> O%s </th>
                        <th align='center'> O%d </th>
                        <th align='center'> O%d </th>
                        <th align='center'> SUM </th>
                    </tr>
            '''%(Result_UnSatisfied_Interpre,Number_Sorted_Array[0],Number_Sorted_Array[1], Number_Sorted_Array[2])
            Count=0
            for i in Rotate_Array:
                Count=Count+1
                Result_UnSatisfied_Interpre ='''%s
                    <tr>
                        <td>%d</td>
                        <td width='260px'>%s</td>
                        <td align='center'>%s</td>
                        <td align='center'>%s</td>
                        <td align='center'>%s</td>
                        <td align='center'>%s</td>
                    </tr>'''%(Result_UnSatisfied_Interpre,Count,i[4],i[0],i[1],i[2],i[3])

            Result_UnSatisfied_Interpre="%s</table>"%Result_UnSatisfied_Interpre


    return
    '''
            <html>

                <body style='font-size:12px;'>

                    <div style="width: 1800px; margin:auto; border:1px solid #ccc;">
                        <div id="col_1" style="float:left;width:240px;">
                            <h3>Concepts: </h3>
                            {result_List}
                            <h3>Ontologies: </h3>
                            {result_List3}
                        </div>
                        <!---
                         <div id="col_2" style="float:left;width:280px;">
                            <h3>All of Interpretations: </h3>
                            {result_List2}
                        </div>
                        --->
                        <div id="col_2" style="float:left;width:270px;">
                            <h3>All of Interpretations (without duplication): </h3>
                            {result_List2_1}
                        </div>
                         <div id="col_4" style="float:left;width:260px;">
                            <h3>Result of statistics: </h3>
                            <p><i>(The satisfaction between each concepts and All Interpretations)</i></p>
                            {html}
                        </div>
                        <div id="col_5" style="float:left;width:260px;">
                            <h3>Select three of Ontologies</h3>
                            <p><i>Using index to select (O3: input 3)</i></p>
                            <form method="post" action=".">
                                <p>O1: <input name="number1"  style="text-align:center;"/></p>
                                <p>O2: <input name="number2"  style="text-align:center;"/></p>
                                <p>O3: <input name="number3" style="text-align:center;"/></p>
                                <p style="text-align: center;"><input type="submit" value="Compute" /></p>
                            </form>
                            <p style="text-align: center;">{result}</p>
                        </div>
                        <div id="col_5" style="float:left;width:400px;">
                            <h4 style="text-align: center;">Statistic of Unsatisfied Interpretations of Three Ontologies</h4>
                            <h5 style="text-align: center;">Counting the unstatisfied number and Ranking Sum</h5>

                            <p>{Result_UnSatisfied_Interpre}</p>
                        </div>
                    </div>
                </body>
            </html>
        '''.format(result_List=result_List,result_List2=result_List2, result_List3=result_List3, html=html,result=result,result_List2_1=result_List2_1,Result_UnSatisfied_Interpre=Result_UnSatisfied_Interpre)
