'''
Created on 20-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
from Database import DataBase
connection=DataBase().connection()
cursor = connection.cursor()
cursor.execute(DataBase().bms_estimator)
results = cursor.fetchall()
for j in results:
	try:
		price= int(j[12])
		totalseats= int(j[13])
		availableseats= int(j[14])
		estimated_collection=""
		est_occupancy=""
		filledseats=(totalseats-availableseats)
		query=""
		if(availableseats<=filledseats):
				est_occupancy=str(100)
				estimated_collection=totalseats*price
				print estimated_collection
				estimated_collection=str(estimated_collection)
				est_occupancy=str(est_occupancy)  
		else:
				bmsoccupancy=(filledseats*100)/totalseats
				print j[0]
				offocc=(availableseats-filledseats)*100/totalseats
				#print offocc
				est_occupancy=(bmsoccupancy+offocc)/2
				#print est_occupancy
				#occupancy=est_occupancy/100
				estimated_collection=(totalseats*price*est_occupancy)/100
				print estimated_collection
				estimated_collection=str(estimated_collection)
				est_occupancy=str(est_occupancy)
				print("===========")
		query="UPDATE collections.bms_theatre_show_collections SET occupancy='"+est_occupancy+"'"+ ",collection='"+estimated_collection+"'"+" WHERE id="+str(j[0])    
		print query
		try:
			cursor.execute(query)
			connection.commit()
			
		except connection.Error as error:
				print(error)
	except:
		""
connection.close()