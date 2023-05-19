% Load the ULog Files
ulog_obj= ulogreader("Ulog-files/TestDatenKönig/log_111_2023-4-14-15-19-36.ulg");
tmp = ulog_obj.readTopicMsgs(); % Just for viewing the values manually

veh_glob_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_global_position").TopicMessages{1, 1};
veh_loc_position = ulog_obj.readTopicMsgs("TopicNames","vehicle_local_position").TopicMessages{1, 1};
battery_status = ulog_obj.readTopicMsgs("TopicNames","battery_status").TopicMessages{1, 1};
actuators_output = ulog_obj.readTopicMsgs("TopicNames","actuator_outputs").TopicMessages{1, 1};
veh_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1}.xyz;
ang_acc = ulog_obj.readTopicMsgs("TopicNames","vehicle_angular_acceleration").TopicMessages{1, 1}.xyz;
subplot(3, 1, 1)
geoplot(veh_glob_position.lat, veh_glob_position.lon)
title("Map View for flight")
subplot(3, 1, 2)
plot(veh_glob_position.timestamp_sample, veh_glob_position.alt)
title("Global Altitude");
ylabel("Altitude in m");
xlabel("Time");
subplot(3, 1, 3)
plot(actuators_output.timestamp, actuators_output.output(:, 5))
title("Magnet Output")
xlabel("Time")
ylabel("PWM us")
ylim([900 2200])
