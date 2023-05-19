% Load the ULog Files
ulog_obj= ulogreader("Ulog-files/TestDatenKönig/log_111_2023-4-14-15-19-36.ulg");
tmp = ulog_obj.readTopicMsgs(); % Just for viewing the values manually

veh_glob_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_global_position").TopicMessages{1, 1};
veh_loc_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_local_position").TopicMessages{1, 1};
battery_status = ulog_obj.readTopicMsgs("TopicNames","battery_status").TopicMessages{1, 1};
actuators_output = ulog_obj.readTopicMsgs("TopicNames","actuator_outputs").TopicMessages{1, 1};
veh_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
ang_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1};

subplot(3, 1, 1)
plot(actuators_output.timestamp, actuators_output.output(:, 1:4))
title("Motor Outputs")
xlabel("Time")
legend("1", "2", "3", "4")
ylabel("PWM us")
ylim([900 2200])

subplot(3, 1, 2)
plot(veh_acc.timestamp, -veh_acc.xyz)
legend("x", "y", "z")
ylabel("Acceleration in m/s")
xlabel("Time")
title("Accelerations")

%{ 
plot(veh_glob_position.timestamp_sample, veh_glob_position.alt)
title("Global Altitude");
ylabel("Altitude in m");
xlabel("Time");
%}

subplot(3, 1, 3)
yyaxis left
plot(battery_status.timestamp, battery_status.discharged_mah);
title("Battery Discharge")
ylabel("mAh")
ylim([0 1800])
xlabel("Time")
hold on

dmAh = gradient(battery_status.discharged_mah);
%max_dmAh = max(gradient(battery_status.discharged_mah));
%imax_dmAh = find(dmAh == max_dmAh);
yyaxis right
plot(battery_status.timestamp, dmAh)
ylabel("delta mAh")
%text(battery_status.timestamp(imax_dmAh), battery_status.discharged_mah(imax_dmAh), '\leftarrow Maximale Steigung '+ string(max_dmAh)+ " bei " + string(battery_status.timestamp(imax_dmAh)));
%datatip(batplot, "DataIndex", find(dmAh == max_dmAh), "Location","northwest");
