
Nosso exemplo de aggregate 

db.Requerentes.aggregate([
  {
    $match: {
      _id: ObjectId("656f179c02210e1a1af60331") 
    }
  },<br>
  {
    $lookup: {
      from: "Produtos", 
      localField: "alimento",
      foreignField: "nome",
      as: "produto"
    }
  },<br>
  {
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


