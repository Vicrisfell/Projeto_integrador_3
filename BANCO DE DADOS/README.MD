
Nosso exemplo de aggregate 

db.Requerentes.aggregate([<br>
  {<br>
    $match: {<br>
      _id: ObjectId("656f179c02210e1a1af60331") <br>
    }<br>
  },<br>
  {<br>
    $lookup: {<br>
      from: "Produtos", <br>
      localField: "alimento",<br>
      foreignField: "nome",<br>
      as: "produto"<br>
    }<br>
  },<br>
  {<br>
    $unwind: "$produto"
  },
  {
    $set: {
      "produto.nome": "Feijão" 
    }
  },
  {<br>
    $merge: {
      into: "Requerentes", 
      whenMatched: "merge", 
      whenNotMatched: "insert" 
    }
  }
]);


