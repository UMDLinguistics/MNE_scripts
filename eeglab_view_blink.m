%%View MEG .fif data in EEGLAB after automatic artifact rejection to
%%manually assess algorithm performance


function eeglab_view_blink(expt,subjID,paradigmName,sampleRate)

global meg_data

%%Load raw MEG data
meg_file = strcat('/Volumes/CUTTLEFISH/MEG_Experiments/',expt,'/data/',subjID,'/',subjID,'_',paradigmName,'-Filtered_raw.fif')
meg_ds = fiff_setup_read_raw(meg_file);
meg_data = fiff_read_raw_segment(meg_ds,meg_ds.first_samp,meg_ds.last_samp);

%%Import MEG data to EEGLAB
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_importdata('dataformat','array','nbchan',0,'data','meg_data','setname',subjID,'srate',sampleRate,'pnts',0,'xmin',0);

%%Import post-blink-rejection events
EEG = pop_importevent( EEG, 'event',strcat('/Volumes/CUTTLEFISH/MEG_Experiments/',expt,'/data/',subjID,'/eve/',subjID,'_',paradigmName,'ModRej.eve'),'fields',{'sample' 'latency' 'null' 'type'},'timeunit',1,'optimalign','off');

%%plot the data
eegplot(EEG.data, 'events', EEG.event, 'srate',sampleRate,'dispchans',30,'title','All data')
eegplot(EEG.data([1 2 3 22 23 24 25 42 43 44 45 60 61 62 63 64 83 84 85 101],:,:), 'events',EEG.event,'srate',sampleRate,'title','blink channels')


