module.exports = {
    users : async (id,io)=>{
        let anotherSocketId = null;
        var allSockets = await io.fetchSockets();
        allSockets.forEach(v=>{
            if(v.customId==id)
            {
                anotherSocketId = v.id
            }
        })
        if(anotherSocketId!=null)
        {
            io.sockets.socket(anotherSocketId).emit('Update');
        }
    },
}