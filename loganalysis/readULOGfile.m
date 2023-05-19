% Load the ULog Files
ulog_wo_load = ulogreader("Ulog-files/TestDatenKönig/log_110_2023-4-14-14-58-44.ulg").readTopicMsgs();
%acc_wo_load = ulogOBJ_wo_load.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
ulog_with_load = ulogreader("Ulog-files/TestDatenKönig/log_111_2023-4-14-15-19-36.ulg").readTopicMsgs();
%acc_with_load = ulogOBJ_with_load.readTopicMsgs("TopicNames","vehicle_acceleration").TopicMessages{1, 1};
