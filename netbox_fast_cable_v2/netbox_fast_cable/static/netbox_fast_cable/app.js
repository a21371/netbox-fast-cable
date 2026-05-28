let A=null;
let B=null;

async function loadDevices(){
    const res = await fetch("/plugins/fast-cable/api/devices/");
    const data = await res.json();

    const a = document.getElementById("devA");
    const b = document.getElementById("devB");

    data.devices.forEach(d=>{
        a.innerHTML += `<option value="${d.id}">${d.name}</option>`;
        b.innerHTML += `<option value="${d.id}">${d.name}</option>`;
    });

    a.onchange = ()=>loadInterfaces("A", a.value);
    b.onchange = ()=>loadInterfaces("B", b.value);
}

async function loadInterfaces(side, deviceId){
    const res = await fetch(`/plugins/fast-cable/api/interfaces/${deviceId}/`);
    const data = await res.json();

    const container = side==="A" ? "ifA":"ifB";
    const div = document.getElementById(container);
    div.innerHTML = "";

    data.interfaces.forEach(i=>{
        const el = document.createElement("div");
        el.innerText = i.name + (i.connected ? " (used)" : "");
        el.style.cursor = "pointer";
        el.style.padding = "4px";
        el.style.border = "1px solid #ccc";

        el.onclick = ()=>{
            if(side==="A") A=i.id;
            else B=i.id;

            el.style.background = "lightgreen";
        };

        div.appendChild(el);
    });
}

async function createCable(){
    const res = await fetch("/plugins/fast-cable/api/create-cable/", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": window.CSRF_TOKEN
        },
        body: JSON.stringify({a:A,b:B})
    });

    const data = await res.json();
    alert(JSON.stringify(data));
}

loadDevices();
