s.boot;

SynthDef(\algo,{
	arg nota=0;
	var gen,env,salida;
	gen = 0.9*SinOsc.ar(220.0*(2.0**(nota/12.0)))+0.1*SinOsc.ar(220.0*(2.0**(nota/12.0+1.0)));
	env = EnvGen.ar(Env.perc,doneAction:2);
	salida = 0.3*gen*env;
	Out.ar(0,salida);
}).add;

x = OSCFunc( { arg msg, time, addr, port;
	msg.removeAt(0);
	Pbind(
		\instrument,\algo,
		\nota,Pseq(msg[0,2..],inf),
		\dur, Pseq(msg[1,3..],inf)
	).play;
}, '/print');
