const db = require('../mysql');
const send = require('./send');
const {mailer} = require('./mailer');

const { sendClientNotif } = require('./notification');
const fetch = require('node-fetch');

exports.login = async (req,res)=> {
    const {email,pass} = req.body
    let query = "select * from allclients where mail = ? and tokens is NULL ";
    let rows = await db.query(query,[email.toLowerCase()])
    console.log(rows)
    if (rows.length ==0)
    {
        res.status(401).end();
    }
    else
    {
        if(rows[0].pass==pass)
        {
            if(rows[0].fname=="")
            {
                res.status(201).send({id:rows[0].id});
            }
            else
            {
                res.status(200).send(rows[0]);
            }
        }
        else
        {
            query = "select * from (select * from users where id not in(select userid from clients)) where mail = ? ";
            rows = await db.query(query,[email.toLowerCase()])
            if(rows.length>0)
            {
                res.status(402).end();
            }
            else
            {
                res.status(404).end();
            }
        }
    }
    res.end();
}
exports.otp = async (req,res)=>{
    const {email,pass} = req.body
    const random = randomint();
    let query = "Replace into users (mail,pass,tokens,tokenid) values (?,?,?,?) ";
    const time  = Date.now()+3*1000*60
    let rows = await db.query(query,[email,pass,random,time]);
    mailer({
        dest:email,
        name:"Client",
        rand:random
    })
    res.status(200).send({id:rows.insertId});
}
exports.check = async (req,res)=>{
    const {id,token} = req.body
    const time= Date.now();
    let query = "select id from users where id =? and tokens = ? and tokenid >= ? ";
    let rows = await db.query(query,[id,token,time]);
    if(rows.length>0)
    {
        res.status(200).end();
    }
    else
    {
        res.status(402).end();
    }
}
exports.signup = async (req,res)=> {
    const {id,name,prename} = req.body
    await db.query("update  users set tokens = NULL ,tokenid=NULL");
    let query = "insert into clients (fname,lname,userid) values (?,?,?)";
    let result = await db.query(query,[name,prename,id])
    query = "select * from allclients where id = ? ";
    result = await db.query(query,[id])
    res.status(200).send(result[0]);
}
exports.sociallogin = async (req,res)=> {
    const {id,fname,lname,mail,picture,provider} = req.body

    let query = "select * from allsocialclients where providerid = ? and provider = ?";
    let rows = await db.query(query,[id,provider])
    if (rows.length ==0)
    {
        try {
            query = "insert into users (mail) values (?)  ";
            rows = await db.query(query,[mail])
            const uid =rows.insertId;
            query = "insert into clients (fname,lname,userid) values (?,?,?) ";
            let result = await db.query(query,[fname,lname,uid])
            query = "insert into socialogin (provider,providerid,userid,picture) values (?,?,?,?)";
            rows = await db.query(query,[provider,id,result.insertId,picture])
            query = "select * from allsocialclients where id = ? ";
            result = await db.query(query,[uid])
            res.status(200).send(result[0]);
        } catch (error) {
            console.log(error)
            res.status(401).send("Mail already existe");
        }
    }
    else
    {
        res.status(200).send(rows[0]);
    }
    res.end();
}
exports.categorieswithsubs = async (req,res)=>{
    //let query = "select *,CONCAT('[',(select GROUP_CONCAT(JSON_OBJECT('id',id,'title',title,'image',image,'globid',globid,'catid',catid) SEPARATOR ', ') from subcategories where ct.id = catid ),']') as subs from categories ct";
    let query = 'SELECT * From allusefulcategorie';
    const row = await db.query(query);
    res.status(200).json(row)
    res.end();
}
exports.getAllProduit = async (req,res)=>{
    const {id,bool} = req.body
    if(bool)
    {
        let query = "SELECT *,JSON_ARRAY(plugins) as plugins FROM produitglobal where catid =? order by RAND() limit 10";
        const a = await db.query(query,[id])
        res.status(200).send(a)
    }
    else
    {
        let query = "SELECT *,JSON_ARRAY(plugins) as plugins FROM produitglobal order by RAND() limit 10"
        const a = await db.query(query)

        res.status(200).send(a)
    }
    res.end();
}
exports.allservices = async (req,res) =>{
    let query = "SELECT servid,adress,service,image,maps,categories from allservices";
    const a = await db.query(query);
    res.status(200).send(a);
}
exports.allservicesbyid = async (req,res) =>{
    const {id} = req.body
    let query = "SELECT servid,adress,service,image,maps,categories from allservices where servid = ?";
    const a = await db.query(query,[id]);
    res.status(200).send(a[0]);
}
exports.getAllMenu = async (req,res) =>{
	const row = await db.query("SELECT * from allusefulcategorie")
	res.status(200).send(row);
	res.end();
}
exports.searchProduit = async (req,res) =>{
	const {id,hint,start} = req.body
	if(id!=-1)
	{
		const row = await db.query("SELECT * from produitglobal where catid = "+id+"  AND (title LIKE '%"+hint+"%' OR details LIKE '%"+hint+"%') limit "+start+",10");
		res.status(200).send(row);
	}
	else
	{
		const row = await db.query("SELECT * from produitglobal where title LIKE '%"+hint+"%' OR details LIKE '%"+hint+"%' limit "+start+",10");
		res.status(200).send(row);
	}
	res.end();
}
exports.getMenu = async (req,res) =>{
    const {sid,cid} = req.body
	const row = await db.query("SELECT * from globalmenu where servid = ? and catid = ?",[sid,cid])
	res.status(200).send(row);
	res.end();
}
exports.getProduit = async (req,res) =>{
    const {mid} = req.body
	const row = await db.query("SELECT * from produitglobal where menuid = ? and title <> '' and prix > 0",[mid])
	res.status(200).send(row);
	res.end();
}
exports.addtopannier = async (req,res) =>{
    const {cid,sid,pid,Q,maps} = req.body
    let condition = await db.query("select quantite from produit where id = ?",[pid])
    condition = condition[0].quantite;
    if(condition>Q || condition ==-1)
    {
        let row = await db.query("SELECT * from pannier where clientid = ? and serviceid = ? and commander = false",[cid,sid])
        let id = -1;
        if(row.length == 0)
        {
            let map = JSON.parse((await db.query('SELECT maps from services where id = ?',[sid]))[0].maps);
            console.log(map.latitude,map.longitude,maps.latitude,maps.longitude);
            let d = (await getDistanceOneToOne(map.latitude,map.longitude,maps.latitude,maps.longitude)).distance.value;
            let tr=0;
            console.log(d);
            tr += Math.max(d%1000,Math.min(d/1000*1000,1000))*0.12;
            d=Math.max(d-1000,0);
            tr += Math.max(d%500,Math.min(d/500*500,500))*0.05;
            d=Math.max(d-500,0);
            tr += d*0.03;
            tr = Math.max(tr,75);
            tr= Math.min(tr,250);
            row = await db.query('INSERT INTO pannier (clientid,serviceid,maps,prix) values (?,?,?,?)',[cid,sid,JSON.stringify(maps),tr])
            id= row.insertId
        }
        else
        {
            id = row[0].id;
        }
        row = await db.query("select * from command where produitid = ?",[pid])
        if(row.length==0)
        {
            row = await db.query('INSERT INTO command (quantite,produitid,pannierid) values (?,?,?)',[Q,pid,id])    
        }
    }
    else 
    {
        res.status(202).send();
    }
	res.end();
}
exports.insert = async (req,res,io) =>{
    const {command,id} = req.body
    const ids = (await db.query('select id from config ORDER BY id DESC LIMIT 1'))[0].id
    let query = 'UPDATE pannier set commander = true , dates=?,config = ?  where id = ?'
    db.query(query,[Date.now(),ids,id]);
    command.forEach(e => {
        db.query('UPDATE command set quantite = ? where id = ?',[e.quantite,e.id])
    });
    res.end();
    const row = (await db.query('select s.userid,p.id from services s join pannier p on(p.serviceid=s.id) where p.id = ?',[id]))[0]
    sendClientNotif(row.userid,'Vous avez recu un nouvelle command N° '+row.id);
    send.users(row.userid,io)
}
exports.archive=  async (req,res)=>{
    const {cid} = req.body;
    const row = await db.query('SELECT * FROM archive where cid = ? and step =1 or step = 6',[cid]);
    res.status(200).send(row)
    res.end();
}
exports.deletes = async (req,res)=>{
    const {pid} = req.body
    await db.query('delete from pannier where id = ?',[pid]);
    res.send();
}
exports.getConfig = async (req,res)=>{
    const row = await db.query('select * from config ORDER BY id DESC LIMIT 1')
    res.send(row[0]);
}
exports.getPannier= async (req,res)=>{
    const {cid} = req.body
    let row = await db.query("SELECT p.id,p.serviceid,JSON_OBJECT('id',d.id,'image',d.image,'driver',d.driver,'material',d.material,'phone',d.phone) as auto,s.service,p.prix,s.maps as map,s.online,p.driveracc+p.servicesend+p.driverfinich+p.clientend+p.commander+p.serviceacc as step,p.commander,p.serviceacc,sum(c.quantite) as max,p.driveracc,p.servicesend,p.driverfinich,p.clientend,p.maps,p.dates,concat('[',group_concat(JSON_OBJECT('id',c.id,'quantite',c.quantite,'pid',pr.id,'title',pr.title,'prix',IF(pr.promo = -1 ,pr.prix,pr.promo),'plugins',pr.plugins,'produitQ',pr.quantite)),']') as commands FROM pannier p join command c on (p.id=c.pannierid) JOIN produit pr on(c.produitid=pr.id) join services s on(p.serviceid=s.id) left join drivers d on(p.driverid=d.id) where p.clientid = ?   GROUP BY p.id",[cid])
    console.log(cid)
    let row2 = await db.query("SELECT p.id as aid,JSON_OBJECT('id',d.id,'image',d.image,'driver',d.driver,'material',d.material,'phone',d.phone) as auto,p.step,p.commands,pid as id from archive p left join drivers d on(p.did=d.id) where p.cid = ? and step!=2 and step!=6   GROUP BY p.id",[cid])
    res.status(200).send([...row,...row2])
}
exports.getCountPannier = async (req,res)=>{
    const {cid,sid} = req.body
    let row = await db.query("SELECT p.id,count(c.id) as qnt FROM pannier p join command c on (p.id=c.pannierid) where p.clientid = ? and p.serviceid=? and p.commander = false  GROUP BY p.id",[cid])
    res.end();
}
exports.phone = async (req,res)=>{
    const {id,phone} = req.body;
    await db.query('UPDATE clients SET phone = ? where id =?',[id,phone]);
    res.end()
}
exports.end=  async (req,res)=>{
    const {pid,drate,srate} = req.body;
	await db.query("UPDATE archive set drate=? ,srate = ? , step=6 where pid = ?",[drate,srate,pid])
    res.end();
}
async function getDistanceOneToOne(lat1, lng1, lat2, lng2)
{
    const Location1Str = lat1 + "," + lng1;
    const Location2Str = lat2 + "," + lng2;
	console.log(Location1Str+" "+Location2Str)
    const GOOGLE_API_KEY = "AIzaSyc_zxzJQEuXgubDZ8VA"
    let ApiURL = "https://maps.googleapis.com/maps/api/directions/json?";

    let params = `origin=${Location1Str}&destination=${Location2Str}&key=${GOOGLE_API_KEY}`; // you need to get a key
    let finalApiURL = `${ApiURL}${encodeURI(params)}`;

    let fetchResult =  await fetch(finalApiURL); // call API
    let Result =  await fetchResult.json(); // extract json
    return Result.routes[0].legs[0];
}
function randomint()
{
    var a="",h,i,b;
    for (i=1;i<7;i++)
    {
        h = Math.pow(10,i)
        b = Math.floor(Math.random()*10)
        a+=b.toString();
    }
    return a;
}